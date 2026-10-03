"""Bound HTTP bodies before JSON or multipart parsers can allocate/spool them."""
import json
import tempfile
from typing import Any, Callable

DEFAULT_MAX_BODY_BYTES = 1024 * 1024
DEFAULT_MAX_UPLOAD_BYTES = 51 * 1024 * 1024  # 50 MiB video plus multipart overhead.
DEFAULT_MAX_PHOTO_BYTES = 6 * 1024 * 1024
MEMORY_BYTES = 1024 * 1024
REPLAY_CHUNK_BYTES = 64 * 1024
MEDIA_UPLOAD_PATH = '/api/settings/ministries-presentation/upload-media'
PHOTO_UPLOAD_PATHS = frozenset({
    '/api/settings/pastoral-team/upload-photo',
    '/api/settings/ministries-presentation/upload-photo',
    '/api/settings/gallery/upload-photo',
})


class RequestBodyLimitMiddleware:
    def __init__(self, app, *, max_body_bytes: int = DEFAULT_MAX_BODY_BYTES,
                 max_upload_bytes: int = DEFAULT_MAX_UPLOAD_BYTES,
                 memory_bytes: int = MEMORY_BYTES,
                 upload_authorizer: Callable[[dict[str, Any]], bool] | None = None):
        if min(max_body_bytes, max_upload_bytes, memory_bytes) <= 0:
            raise ValueError('Request size limits must be positive')
        self.app = app
        self.max_body_bytes = max_body_bytes
        self.max_upload_bytes = max_upload_bytes
        self.memory_bytes = min(memory_bytes, MEMORY_BYTES)
        self.upload_authorizer = upload_authorizer

    @staticmethod
    def _is_upload(scope: dict[str, Any]) -> bool:
        path = scope.get('path', '').rstrip('/')
        return scope.get('method') == 'POST' and (path == MEDIA_UPLOAD_PATH or path in PHOTO_UPLOAD_PATHS)

    def _limit(self, scope: dict[str, Any]) -> int:
        if scope.get('method') == 'POST':
            path = scope.get('path', '').rstrip('/')
            if path == MEDIA_UPLOAD_PATH:
                return self.max_upload_bytes
            if path in PHOTO_UPLOAD_PATHS:
                return min(self.max_upload_bytes, DEFAULT_MAX_PHOTO_BYTES)
        return self.max_body_bytes

    @staticmethod
    async def _reject(send, status: int):
        detail = {413: 'Pedido demasiado grande.', 400: 'Content-Length inválido.',
                  401: 'Autenticação necessária.'}[status]
        body = json.dumps({'detail': detail}, ensure_ascii=False).encode('utf-8')
        headers = [(b'content-type', b'application/json; charset=utf-8'),
                   (b'content-length', str(len(body)).encode('ascii')),
                   (b'cache-control', b'private, no-store'),
                   (b'x-content-type-options', b'nosniff')]
        if status == 401:
            headers.append((b'www-authenticate', b'Bearer'))
        await send({
            'type': 'http.response.start', 'status': status,
            'headers': headers,
        })
        await send({'type': 'http.response.body', 'body': body})

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        if self.upload_authorizer is not None and self._is_upload(scope):
            if self.upload_authorizer(scope) is not True:
                await self._reject(send, 401)
                return
        limit = self._limit(scope)
        lengths = [value for name, value in scope.get('headers', []) if name.lower() == b'content-length']
        if lengths:
            if len(lengths) != 1 or not lengths[0].isdigit():
                await self._reject(send, 400)
                return
            # Avoid converting arbitrarily long integer strings supplied by a client.
            if len(lengths[0]) > 20 or int(lengths[0]) > limit:
                await self._reject(send, 413)
                return

        # Context manager also closes rolled-over files on cancellation and app errors.
        with tempfile.SpooledTemporaryFile(max_size=self.memory_bytes, mode='w+b') as body_file:
            size = 0
            rolled = False
            while True:
                message = await receive()
                if message['type'] == 'http.disconnect':
                    return
                if message['type'] != 'http.request':
                    raise RuntimeError('Unexpected ASGI request event')
                chunk = message.get('body', b'')
                size += len(chunk)
                if size > limit:
                    await self._reject(send, 413)
                    return
                # Roll over BEFORE writing: SpooledTemporaryFile normally writes first,
                # which would briefly retain a large inbound ASGI chunk in BytesIO.
                if not rolled and size > self.memory_bytes:
                    body_file.rollover()
                    rolled = True
                body_file.write(chunk)
                more_body = message.get('more_body', False)
                # Do not retain a large server-owned chunk while parsing/replaying.
                del chunk, message
                if not more_body:
                    break
            body_file.seek(0)
            remaining = size
            replayed = False

            async def replay_receive():
                nonlocal remaining, replayed
                if replayed:
                    # Preserve disconnect notifications for streaming responses.
                    return await receive()
                chunk = body_file.read(min(REPLAY_CHUNK_BYTES, remaining))
                remaining -= len(chunk)
                replayed = remaining == 0
                return {'type': 'http.request', 'body': chunk, 'more_body': not replayed}

            await self.app(scope, replay_receive, send)
