"""Gateway and upload regressions. All provider traffic uses an in-process transport."""
import io
import asyncio
import json
import logging
import os
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import httpx
from fastapi import HTTPException, UploadFile, Request
from cryptography.fernet import Fernet
from sqlmodel import SQLModel, Session, create_engine
from app.models import PaymentAttempt
from PIL import Image
from pydantic import ValidationError

from app.routers import donations
from app import validators
from app.gateway import _gateway_request

BASE = 'https://api.ifthenpay.com/spg/payment'
KEY = 'test-merchant-sensitive'
REQUEST_ID = 'i2szvoUfPYBMWdSxqO3n'


class GatewayConfigTests(unittest.TestCase):
    def test_rejects_noncanonical_gateway_destinations(self):
        for url in ['http://api.ifthenpay.com/spg/payment', 'http://127.0.0.1',
                    'https://api.ifthenpay.com.evil.test/spg/payment',
                    'https://api.ifthenpay.com@evil.test/spg/payment',
                    BASE + '?redirect=evil', BASE + '/../../evil',
                    BASE + '#fragment', 'https://api.ifthenpay.com:444/spg/payment']:
            with self.subTest(url=url), self.assertRaises(HTTPException):
                validators.validate_ifthenpay_config({'api_base': url})

    def test_accepts_official_base_and_legacy_alias(self):
        self.assertEqual(validators.validate_sibs_config({'sibs_api_base': BASE + '/'})['api_base'], BASE)

    def test_legacy_database_config_is_revalidated(self):
        setting = SimpleNamespace(value=json.dumps({'sibs_api_base': 'http://127.0.0.1', 'sibs_client_id': KEY}))
        with patch.object(donations, 'get_setting', return_value=setting):
            with self.assertRaises(HTTPException) as caught:
                donations.get_ifthenpay_credentials(None)
        self.assertEqual(caught.exception.status_code, 503)

    def test_rejects_invalid_amounts_without_rounding(self):
        for amount in [float('inf'), float('nan'), '0.001', '1.005', True, '1000000000000000000000']:
            with self.subTest(amount=str(amount)), self.assertRaises(ValidationError):
                donations.DonationRequest(amount=amount, phone='912345678')

    def test_rejects_unsafe_contact_fields(self):
        for fields in [{'phone': 'abc912345678'}, {'phone': '９１２３４５６７８'},
                       {'email': 'someone@example.com\r\nBcc: other@example.com'},
                       {'description': 'hello\x00world'}, {'category': 'x' * 101}]:
            with self.subTest(fields=list(fields)), self.assertRaises(ValidationError):
                donations.DonationRequest(**({'amount': '1.20', 'phone': '912345678'} | fields))


class GatewayRequestTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client_type = httpx.AsyncClient
        setting = SimpleNamespace(value=json.dumps({'api_base': BASE, 'mbway_key': KEY}))
        self.setting_patch = patch.object(donations, 'get_setting', return_value=setting)
        self.setting_patch.start()
        self.addCleanup(self.setting_patch.stop)

    def provider(self, handler):
        transport = httpx.MockTransport(handler)
        return patch('httpx.AsyncClient', side_effect=lambda **kw: self.client_type(transport=transport, **kw))

    async def isolated_request(self, status_id=None):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {'SETTINGS_ENCRYPTION_KEY': Fernet.generate_key().decode()}):
            engine = create_engine('sqlite:///' + str(Path(directory) / 'payments.db'))
            SQLModel.metadata.create_all(engine)
            try:
                with Session(engine) as session:
                    key = str(uuid.uuid4())
                    if status_id is not None:
                        session.add(PaymentAttempt(key=key, fingerprint='test', client_fingerprint='test',
                                                  phone_fingerprint='test', created_at=0, order_id='test',
                                                  state='ready', request_id=status_id))
                        session.commit()
                        return await donations.payment_status(status_id, session, key)
                    request = Request({'type': 'http', 'client': ('testclient', 1234)})
                    return await donations.donate_mbway(
                        donations.DonationRequest(amount='1.20', phone='+351 912 345 678'), request, session, key)
            finally:
                engine.dispose()

    async def donate(self):
        return await self.isolated_request()

    async def status(self, request_id=REQUEST_ID):
        return await self.isolated_request(request_id)

    async def test_valid_request_preserves_exact_amount_and_contract(self):
        def handle(request):
            payload = json.loads(request.content)
            self.assertEqual(payload['amount'], '1.20')
            self.assertEqual(payload['mobileNumber'], '351#912345678')
            self.assertEqual(str(request.url), BASE + '/mbway')
            return httpx.Response(200, json={'Status': '000', 'Message': 'Pending', 'RequestId': REQUEST_ID, 'Amount': 1.2})
        with self.provider(handle):
            result = await self.donate()
        self.assertTrue(result['ok'])
        self.assertEqual(result['requestId'], REQUEST_ID)
        self.assertEqual(result['amount'], 1.2)

    async def test_malformed_provider_responses_are_safe_gateway_errors(self):
        for body in [[], None, {}, {'Status': '000', 'RequestId': None},
                     {'Status': '000', 'Message': 'Pending', 'RequestId': REQUEST_ID, 'Amount': 2},
                     {'Status': {}, 'Message': KEY}]:
            with self.subTest(body_type=type(body).__name__), self.provider(lambda req: httpx.Response(200, json=body)):
                with self.assertRaises(HTTPException) as caught:
                    await self.donate()
                self.assertEqual(caught.exception.status_code, 502)
                self.assertNotIn(KEY, caught.exception.detail)

    async def test_provider_error_body_is_not_logged_or_returned(self):
        with self.provider(lambda req: httpx.Response(500, text=KEY)), self.assertLogs(level=logging.DEBUG) as logs:
            with self.assertRaises(HTTPException) as caught:
                await self.donate()
        self.assertNotIn(KEY, '\n'.join(logs.output) + caught.exception.detail)

    async def test_provider_decline_message_is_not_logged_or_returned(self):
        with self.provider(lambda req: httpx.Response(200, json={'Status': '999', 'Message': KEY})), self.assertLogs(level=logging.DEBUG) as logs:
            with self.assertRaises(HTTPException) as caught:
                await self.donate()
        self.assertEqual(caught.exception.status_code, 400)
        self.assertNotIn(KEY, '\n'.join(logs.output) + caught.exception.detail)

    async def test_network_exception_does_not_log_sensitive_url(self):
        def handle(request):
            raise httpx.ConnectError('failure ' + KEY, request=request)
        with self.provider(handle), self.assertLogs(level=logging.DEBUG) as logs:
            with self.assertRaises(HTTPException):
                await self.donate()
        self.assertNotIn(KEY, '\n'.join(logs.output))

    async def test_status_query_secret_is_not_logged(self):
        with self.provider(lambda req: httpx.Response(200, json={'Status': '000', 'Message': 'Success', 'RequestId': REQUEST_ID})), self.assertLogs(level=logging.DEBUG) as logs:
            result = await self.status()
        self.assertEqual(result['Status'], '000')
        self.assertNotIn(KEY, '\n'.join(logs.output))
        self.assertNotIn(REQUEST_ID, '\n'.join(logs.output))

    async def test_transport_logs_redact_wire_headers_and_restore_context(self):
        def handle(request):
            logging.getLogger('httpcore.http11').debug('headers=%s', KEY)
            return httpx.Response(200, json={'Status': '000', 'Message': 'Pending', 'RequestId': REQUEST_ID, 'Amount': 1.2})
        with self.provider(handle), self.assertLogs(level=logging.DEBUG) as logs:
            await self.donate()
            logging.getLogger('httpx').info('unrelated request diagnostic')
        self.assertNotIn(KEY, '\n'.join(logs.output))
        self.assertIn('unrelated request diagnostic', '\n'.join(logs.output))
        self.assertFalse(_gateway_request.get())

    async def test_gateway_redaction_does_not_change_other_tasks_logs(self):
        started, resume = asyncio.Event(), asyncio.Event()
        async def handle(request):
            started.set()
            await resume.wait()
            logging.getLogger('httpcore.http11').debug('headers=%s', KEY)
            return httpx.Response(200, json={'Status': '000', 'Message': 'Pending', 'RequestId': REQUEST_ID, 'Amount': 1.2})
        with self.provider(handle), self.assertLogs(level=logging.DEBUG) as logs:
            task = asyncio.create_task(self.donate())
            await asyncio.wait_for(started.wait(), timeout=2)
            logging.getLogger('httpx').info('concurrent unrelated diagnostic')
            resume.set()
            await asyncio.wait_for(task, timeout=2)
        self.assertNotIn(KEY, '\n'.join(logs.output))
        self.assertIn('concurrent unrelated diagnostic', '\n'.join(logs.output))

    async def test_provider_response_limit(self):
        with self.provider(lambda req: httpx.Response(200, content=b' ' * 65537)):
            with self.assertRaises(HTTPException) as caught:
                await self.donate()
        self.assertEqual(caught.exception.status_code, 502)

    async def test_unknown_success_message_is_not_treated_as_payment_confirmation(self):
        with self.provider(lambda req: httpx.Response(200, json={'Status': '000', 'Message': 'unrecognized', 'RequestId': REQUEST_ID})):
            with self.assertRaises(HTTPException) as caught:
                await self.status()
        self.assertEqual(caught.exception.status_code, 502)

    async def test_invalid_status_identifier_is_rejected_before_provider_call(self):
        def handle(request):
            self.fail('invalid identifier must not reach provider')
        with self.provider(handle), self.assertRaises(HTTPException) as caught:
            await self.status('x\r\nprivate')
        self.assertEqual(caught.exception.status_code, 400)

    async def test_status_filters_unexpected_provider_fields(self):
        with self.provider(lambda req: httpx.Response(200, json={'Status': '000', 'Message': 'Success', 'RequestId': REQUEST_ID, 'mbWayKey': KEY, 'email': 'private@example.com'})):
            result = await self.status()
        self.assertNotIn('mbWayKey', result)
        self.assertNotIn('email', result)

    async def test_status_rejects_invalid_json_and_mismatched_identifier(self):
        for response in [httpx.Response(200, text='not json'), httpx.Response(200, json=[]),
                         httpx.Response(200, json={'Status': '000', 'Message': 'Success', 'RequestId': 'different'})]:
            with self.provider(lambda req: response), self.assertRaises(HTTPException) as caught:
                await self.status()
            self.assertEqual(caught.exception.status_code, 502)

    async def test_gateway_redirect_is_not_followed(self):
        calls = []
        def handle(request):
            calls.append(str(request.url))
            return httpx.Response(307, headers={'location': 'https://evil.test/'})
        with self.provider(handle), self.assertRaises(HTTPException):
            await self.donate()
        self.assertEqual(calls, [BASE + '/mbway'])


class UploadTests(unittest.IsolatedAsyncioTestCase):
    async def test_video_read_is_bounded_before_rejection(self):
        class LargeVideo:
            filename = 'huge.mp4'
            async def read(self, size=-1):
                if size != 65:
                    raise AssertionError('Video reads must request at most limit plus one')
                return b'x' * size
        with TemporaryDirectory() as directory, patch.object(validators, 'MAX_VIDEO_UPLOAD_SIZE', 64):
            with self.assertRaises(HTTPException):
                await validators.save_and_validate_media(LargeVideo(), Path(directory))
            self.assertEqual(list(Path(directory).iterdir()), [])

    async def test_decompression_bomb_warning_is_rejected(self):
        data = io.BytesIO()
        Image.new('RGB', (4, 4)).save(data, format='PNG')
        for save in [validators.save_and_validate_image, validators.save_and_validate_media]:
            with TemporaryDirectory() as directory, patch.object(Image, 'MAX_IMAGE_PIXELS', 10):
                with self.assertRaises(HTTPException):
                    await save(UploadFile(io.BytesIO(data.getvalue()), filename='test.png'), Path(directory))
                self.assertEqual(list(Path(directory).iterdir()), [])

    async def test_supported_video_container_headers_are_saved(self):
        # Container recognition fixtures, not claims of codec/frame validation.
        mp4 = b'\x00\x00\x00\x18ftypisom\x00\x00\x00\x00isommp42'
        webm = b'\x1a\x45\xdf\xa3\x87\x42\x82\x84webm'
        for filename, contents in [('test.mp4', mp4), ('test.webm', webm)]:
            with TemporaryDirectory() as directory:
                result = await validators.save_and_validate_media(UploadFile(io.BytesIO(contents), filename=filename), Path(directory))
                self.assertEqual(result['mediaType'], 'video')
                self.assertEqual((Path(directory) / result['filename']).read_bytes(), contents)

    async def test_upload_read_is_bounded_before_rejection(self):
        class RecordingUpload:
            filename = 'huge.png'
            reads = []
            async def read(self, size=-1):
                self.reads.append(size)
                return b'x' * 33
        for save in [validators.save_and_validate_image, validators.save_and_validate_media]:
            upload = RecordingUpload()
            upload.reads = []
            with TemporaryDirectory() as directory, patch.object(validators, 'MAX_UPLOAD_SIZE', 32):
                with self.assertRaises(HTTPException):
                    await save(upload, Path(directory))
                self.assertEqual(upload.reads, [33])
                self.assertEqual(list(Path(directory).iterdir()), [])

    async def test_fake_video_is_rejected(self):
        for filename in ['bad.mp4', 'bad.webm']:
            with TemporaryDirectory() as directory:
                upload = UploadFile(io.BytesIO(b'<html>not video</html>'), filename=filename)
                with self.assertRaises(HTTPException):
                    await validators.save_and_validate_media(upload, Path(directory))
                self.assertEqual(list(Path(directory).iterdir()), [])

    async def test_real_png_upload_is_preserved(self):
        data = io.BytesIO()
        Image.new('RGB', (2, 2)).save(data, format='PNG')
        for save in [validators.save_and_validate_image, validators.save_and_validate_media]:
            with TemporaryDirectory() as directory:
                result = await save(UploadFile(io.BytesIO(data.getvalue()), filename='test.png'), Path(directory))
                filename = result['filename'] if isinstance(result, dict) else result
                self.assertEqual((Path(directory) / filename).read_bytes(), data.getvalue())


if __name__ == '__main__':
    unittest.main()
