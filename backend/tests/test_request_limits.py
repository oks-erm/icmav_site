"""Pre-parser body limits use real temporary files and an in-process ASGI app."""
import asyncio
import tempfile
import unittest
from unittest.mock import patch

from app.request_limits import RequestBodyLimitMiddleware


class RequestLimitTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sent = []
        self.received = []
        self.called = False
        self.files = []
        real_spool = tempfile.SpooledTemporaryFile
        def tracked_spool(*args, **kwargs):
            file = real_spool(*args, **kwargs)
            original_write = file.write
            def bounded_write(data):
                # Catch automatic rollover after a large in-memory write.
                if not file._rolled:
                    self.assertLessEqual(file.tell() + len(data), kwargs['max_size'])
                return original_write(data)
            file.write = bounded_write
            self.files.append(file)
            return file
        self.spool_patch = patch('app.request_limits.tempfile.SpooledTemporaryFile', side_effect=tracked_spool)
        self.spool_patch.start()
        self.addCleanup(self.spool_patch.stop)

    async def app(self, scope, receive, send):
        self.called = True
        while True:
            message = await receive()
            self.received.append(message)
            if not message.get('more_body', False):
                break
        await send({'type': 'http.response.start', 'status': 200, 'headers': []})
        await send({'type': 'http.response.body', 'body': b'ok'})

    async def run_request(self, chunks, *, headers=(), path='/api/admin/login', app=None, upload_authorizer=None):
        iterator = iter(chunks)
        async def receive():
            return next(iterator)
        middleware = RequestBodyLimitMiddleware(app or self.app, max_body_bytes=32, max_upload_bytes=64,
                                               memory_bytes=8, upload_authorizer=upload_authorizer)
        await middleware({'type': 'http', 'path': path, 'method': 'POST', 'headers': list(headers)}, receive, self.send)

    async def send(self, message):
        self.sent.append(message)

    def assert_rejected(self, status=413):
        self.assertFalse(self.called)
        self.assertEqual(self.sent[0]['status'], status)
        headers = dict(self.sent[0]['headers'])
        self.assertEqual(headers[b'cache-control'], b'private, no-store')
        self.assertEqual(headers[b'x-content-type-options'], b'nosniff')
        self.assertTrue(all(file.closed for file in self.files))

    async def test_oversized_content_length_is_rejected_before_reading(self):
        await self.run_request([], headers=[(b'content-length', b'33')])
        self.assert_rejected()
        self.assertEqual(self.files, [])

    async def test_chunked_body_is_counted_before_parser_runs(self):
        await self.run_request([
            {'type': 'http.request', 'body': b'a' * 20, 'more_body': True},
            {'type': 'http.request', 'body': b'b' * 13, 'more_body': False},
        ])
        self.assert_rejected()

    async def test_false_small_content_length_does_not_bypass_count(self):
        await self.run_request([{'type': 'http.request', 'body': b'a' * 33}], headers=[(b'content-length', b'1')])
        self.assert_rejected()

    async def test_exact_limit_is_replayed_without_corrupting_body(self):
        await self.run_request([
            {'type': 'http.request', 'body': b'a' * 16, 'more_body': True},
            {'type': 'http.request', 'body': b'b' * 16, 'more_body': False},
        ])
        self.assertEqual(self.sent[0]['status'], 200)
        self.assertEqual(b''.join(msg['body'] for msg in self.received), b'a' * 16 + b'b' * 16)
        self.assertTrue(self.files[0]._rolled)
        self.assertTrue(self.files[0].closed)

    async def test_upload_route_gets_larger_limit_with_bounded_memory(self):
        await self.run_request([{'type': 'http.request', 'body': b'v' * 64}], path='/api/settings/ministries-presentation/upload-media')
        self.assertEqual(self.sent[0]['status'], 200)
        self.assertEqual(b''.join(msg['body'] for msg in self.received), b'v' * 64)
        self.assertTrue(self.files[0]._rolled)
        self.assertTrue(self.files[0].closed)

    async def test_unauthorized_upload_is_rejected_without_receiving_or_spooling(self):
        for headers in [[], [(b'authorization', b'Bearer invalid')]]:
            self.sent = []
            await self.run_request([], headers=headers, path='/api/settings/ministries-presentation/upload-media',
                                   upload_authorizer=lambda scope: False)
            self.assert_rejected(401)
            self.assertEqual(self.files, [])
            self.assertEqual(dict(self.sent[0]['headers'])[b'www-authenticate'], b'Bearer')

    async def test_authorized_upload_flows_normally(self):
        checked_paths = []
        def authorize(scope):
            checked_paths.append(scope['path'])
            return True
        await self.run_request([{'type': 'http.request', 'body': b'v' * 64}],
                               path='/api/settings/ministries-presentation/upload-media', upload_authorizer=authorize)
        self.assertEqual(checked_paths, ['/api/settings/ministries-presentation/upload-media'])
        self.assertEqual(self.sent[0]['status'], 200)

    async def test_nonupload_requests_do_not_invoke_upload_authorizer(self):
        def authorize(scope):
            self.fail('Upload authorization must not affect login/payment requests')
        for path in ['/api/admin/login', '/api/donate/mbway']:
            self.sent = []
            await self.run_request([{'type': 'http.request', 'body': b'{}'}], path=path, upload_authorizer=authorize)
            self.assertEqual(self.sent[0]['status'], 200)

    async def test_unknown_upload_like_route_does_not_receive_larger_limit(self):
        await self.run_request([{'type': 'http.request', 'body': b'a' * 33}], path='/api/unknown/upload-media')
        self.assert_rejected()

    async def test_oversized_upload_is_rejected(self):
        await self.run_request([{'type': 'http.request', 'body': b'v' * 65}], path='/api/settings/ministries-presentation/upload-media')
        self.assert_rejected()

    async def test_incoming_chunk_is_released_before_parser_runs(self):
        released = []
        class TrackedBytes(bytes):
            def __del__(self):
                released.append(True)
        async def receive():
            return {'type': 'http.request', 'body': TrackedBytes(b'v' * 64)}
        async def downstream(scope, receive, send):
            self.assertEqual(released, [True])
            await self.app(scope, receive, send)
        middleware = RequestBodyLimitMiddleware(downstream, max_body_bytes=64, memory_bytes=8)
        await middleware({'type': 'http', 'path': '/api/admin/login', 'headers': []}, receive, self.send)
        self.assertEqual(self.sent[0]['status'], 200)

    async def test_disconnect_closes_spooled_file_without_calling_app(self):
        await self.run_request([
            {'type': 'http.request', 'body': b'a' * 16, 'more_body': True},
            {'type': 'http.disconnect'},
        ])
        self.assertFalse(self.called)
        self.assertEqual(self.sent, [])
        self.assertTrue(self.files[0].closed)

    async def test_cancelled_receive_closes_file(self):
        calls = 0
        async def receive():
            nonlocal calls
            calls += 1
            if calls == 1:
                return {'type': 'http.request', 'body': b'x' * 16, 'more_body': True}
            raise asyncio.CancelledError
        middleware = RequestBodyLimitMiddleware(self.app, memory_bytes=8)
        with self.assertRaises(asyncio.CancelledError):
            await middleware({'type': 'http', 'path': '/api/admin/login', 'headers': []}, receive, self.send)
        self.assertFalse(self.called)
        self.assertTrue(self.files[0].closed)

    async def test_downstream_error_closes_file(self):
        async def broken_app(scope, receive, send):
            raise RuntimeError('test failure')
        with self.assertRaisesRegex(RuntimeError, 'test failure'):
            await self.run_request([{'type': 'http.request', 'body': b'x' * 16}], app=broken_app)
        self.assertTrue(self.files[0].closed)

    async def test_ambiguous_or_invalid_length_is_rejected(self):
        for headers in [[(b'content-length', b'-1')], [(b'content-length', b'no')],
                        [(b'content-length', b'1'), (b'content-length', b'2')]]:
            self.sent = []
            await self.run_request([], headers=headers)
            self.assert_rejected(400)

    async def test_websocket_scope_is_passed_through(self):
        scope = {'type': 'websocket'}
        async def downstream(actual, receive, send):
            self.assertIs(actual, scope)
            self.called = True
        middleware = RequestBodyLimitMiddleware(downstream)
        await middleware(scope, None, None)
        self.assertTrue(self.called)
        self.assertEqual(self.files, [])


if __name__ == '__main__':
    unittest.main()
