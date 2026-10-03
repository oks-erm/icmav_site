"""Payment retries use disposable SQLite databases and an in-process gateway fake."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import uuid
from threading import Event
import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from cryptography.fernet import Fernet
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.routers import donations
from app.database import get_session


class PaymentAttemptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.engine = create_engine('sqlite:///' + str(Path(self.tmp.name) / 'payments.db'), connect_args={'check_same_thread': False})
        self.addCleanup(self.engine.dispose)
        SQLModel.metadata.create_all(self.engine)
        self.env = patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': Fernet.generate_key().decode()})
        self.env.start()
        self.addCleanup(self.env.stop)
        app = FastAPI()
        app.include_router(donations.router)
        def session():
            with Session(self.engine) as value:
                yield value
        app.dependency_overrides[get_session] = session
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        self.config = patch.object(donations, 'get_ifthenpay_credentials', return_value={
            'api_base': 'https://api.ifthenpay.com/spg/payment', 'mbway_key': 'private-test-key', 'default_email': ''})
        self.credentials = self.config.start()
        self.addCleanup(self.config.stop)
        self.gateway = patch.object(donations, 'gateway_request', new_callable=AsyncMock).start()
        self.addCleanup(patch.stopall)
        self.gateway.return_value = {'Status': '000', 'Message': 'Pending', 'RequestId': 'unpredictable-provider-id', 'Amount': 12.5}
        self.payload = {'amount': '12.50', 'phone': '912345678', 'email': 'private@example.test'}
        self.key = str(uuid.uuid4())

    def post(self, key=None, payload=None):
        return self.client.post('/api/donate/mbway', json=payload or self.payload,
                                headers={'Idempotency-Key': key or self.key})

    def test_replay_and_reload_recover_same_result_without_another_gateway_call(self):
        first = self.post()
        self.assertEqual(first.status_code, 200)
        second = self.post()
        self.assertEqual(second.json(), first.json())
        self.assertEqual(self.gateway.await_count, 1)
        recovered = self.client.get('/api/donate/attempt', headers={'Idempotency-Key': self.key})
        self.assertEqual(recovered.json(), first.json())
        self.assertEqual(self.gateway.await_count, 1)
        with self.engine.connect() as connection:
            rows = connection.exec_driver_sql('select * from paymentattempt').fetchall()
        stored = repr(rows)
        self.assertNotIn('912345678', stored)
        self.assertNotIn('private@example.test', stored)
        self.assertNotIn('private-test-key', stored)

    def test_payload_change_for_same_key_is_rejected(self):
        self.assertEqual(self.post().status_code, 200)
        changed = self.post(payload={**self.payload, 'amount': '20.00'})
        self.assertEqual(changed.status_code, 409)
        self.assertEqual(self.gateway.await_count, 1)

    def test_timeout_cannot_trigger_a_second_gateway_attempt(self):
        self.gateway.side_effect = HTTPException(502, 'Gateway timeout')
        response = self.post()
        self.assertEqual(response.status_code, 502)
        self.assertIsNone(response.headers.get('x-payment-attempt-state'))
        self.assertEqual(self.post().status_code, 409)
        self.assertEqual(self.client.get('/api/donate/attempt', headers={'Idempotency-Key': self.key}).status_code, 409)
        self.assertEqual(self.gateway.await_count, 1)

    def test_invalid_or_missing_key_never_reaches_gateway(self):
        for key in ['', 'easy-to-guess', str(uuid.uuid1())]:
            response = self.client.post('/api/donate/mbway', json=self.payload, headers={'Idempotency-Key': key})
            self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/donate/mbway', json=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.gateway.await_count, 0)

    def test_pending_attempt_is_committed_before_network_and_cannot_be_reclaimed(self):
        async def provider(*args, **kwargs):
            with self.engine.connect() as connection:
                row = connection.exec_driver_sql('select state from paymentattempt').one()
            self.assertEqual(row[0], 'pending')
            from app.payment_attempts import reserve_attempt
            with Session(self.engine) as session:
                with self.assertRaises(HTTPException) as raised:
                    reserve_attempt(session, self.key, {**kwargs['json'], '_category': None}, 'testclient')
            self.assertEqual(raised.exception.status_code, 409)
            return {'Status': '000', 'Message': 'Pending', 'RequestId': 'unpredictable-provider-id', 'Amount': 12.5}
        self.gateway.side_effect = provider
        self.assertEqual(self.post().status_code, 200)
        self.assertEqual(self.gateway.await_count, 1)

    def test_distinct_keys_are_throttled_for_same_phone(self):
        for _ in range(3):
            self.assertEqual(self.post(key=str(uuid.uuid4())).status_code, 200)
        response = self.post(key=str(uuid.uuid4()))
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers.get('x-payment-attempt-state'), 'not-sent')
        self.assertEqual(response.headers.get('retry-after'), '300')
        self.assertEqual(self.gateway.await_count, 3)

    def test_preflight_failure_explicitly_marks_not_sent_but_existing_attempt_never_does(self):
        self.credentials.return_value['mbway_key'] = ''
        response = self.post()
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.headers.get('x-payment-attempt-state'), 'not-sent')
        self.assertEqual(self.gateway.await_count, 0)
        self.credentials.return_value['mbway_key'] = 'private-test-key'
        self.assertEqual(self.post().status_code, 200)
        self.credentials.return_value['mbway_key'] = ''
        response = self.post()
        self.assertEqual(response.status_code, 503)
        self.assertIsNone(response.headers.get('x-payment-attempt-state'))
        self.assertEqual(self.gateway.await_count, 1)

    def test_status_requires_ownership_and_throttles_repeated_provider_reads(self):
        self.assertEqual(self.post().status_code, 200)
        self.gateway.reset_mock()
        self.gateway.return_value = {'Status': '000', 'Message': 'Pending', 'RequestId': 'unpredictable-provider-id'}
        path = '/api/payment-status/unpredictable-provider-id'
        self.assertEqual(self.client.get(path).status_code, 400)
        self.assertEqual(self.client.get(path, headers={'Idempotency-Key': str(uuid.uuid4())}).status_code, 404)
        self.assertEqual(self.gateway.await_count, 0)
        headers = {'Idempotency-Key': self.key}
        self.assertEqual(self.client.get(path, headers=headers).status_code, 200)
        self.assertEqual(self.client.get(path, headers=headers).status_code, 200)
        self.assertEqual(self.gateway.await_count, 1)

        self.assertEqual(self.client.get('/api/payment-status/wrong-provider-id', headers=headers).status_code, 404)
        self.assertEqual(self.gateway.await_count, 1)

    def test_concurrent_submissions_have_only_one_provider_call(self):
        started, release = Event(), Event()
        async def provider(*args, **kwargs):
            started.set()
            await asyncio.to_thread(release.wait, 3)
            return {'Status': '000', 'Message': 'Pending', 'RequestId': 'unpredictable-provider-id', 'Amount': 12.5}
        self.gateway.side_effect = provider
        with ThreadPoolExecutor(max_workers=2) as executor:
            first = executor.submit(self.post)
            try:
                self.assertTrue(started.wait(2))
                second = executor.submit(self.post)
                self.assertEqual(second.result(timeout=2).status_code, 409)
            finally:
                release.set()
            self.assertEqual(first.result(timeout=2).status_code, 200)
        self.assertEqual(self.gateway.await_count, 1)

    def test_ledger_capacity_is_bounded_without_forgetting_old_keys(self):
        with patch('app.payment_attempts.MAX_ATTEMPTS', 1):
            first = self.post()
            self.assertEqual(first.status_code, 200)
            self.assertEqual(self.post(key=str(uuid.uuid4())).status_code, 503)
            self.assertEqual(self.post().json(), first.json())
        self.assertEqual(self.gateway.await_count, 1)

    def test_late_pending_poll_cannot_overwrite_confirmed_success(self):
        self.assertEqual(self.post().status_code, 200)
        self.gateway.reset_mock()
        started, release = Event(), Event()
        async def provider(*args, **kwargs):
            if self.gateway.await_count == 1:
                started.set()
                await asyncio.to_thread(release.wait, 3)
                message = 'Pending'
            else:
                message = 'Success'
            return {'Status': '000', 'Message': message, 'RequestId': 'unpredictable-provider-id'}
        self.gateway.side_effect = provider
        path = '/api/payment-status/unpredictable-provider-id'
        headers = {'Idempotency-Key': self.key}
        future_time = time.time() + 5
        with ThreadPoolExecutor(max_workers=2) as executor:
            old = executor.submit(self.client.get, path, headers=headers)
            try:
                self.assertTrue(started.wait(2))
                with patch('app.payment_attempts.time', SimpleNamespace(time=lambda: future_time)):
                    latest = self.client.get(path, headers=headers)
                self.assertEqual(latest.json()['Message'], 'Success')
            finally:
                release.set()
            self.assertEqual(old.result(timeout=2).json()['Message'], 'Success')
        self.assertEqual(self.client.get(path, headers=headers).json()['Message'], 'Success')
        self.assertEqual(self.gateway.await_count, 2)


if __name__ == '__main__':
    unittest.main()
