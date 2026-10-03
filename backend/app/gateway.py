"""Boundaries for IFTHENPAY configuration, transport and response validation."""
from contextvars import ContextVar
from decimal import Decimal, InvalidOperation
import json
import logging
import re

import httpx
from fastapi import HTTPException

IFTHENPAY_API_BASE = 'https://api.ifthenpay.com/spg/payment'
MAX_RESPONSE_BYTES = 64 * 1024
logger = logging.getLogger(__name__)
_gateway_request = ContextVar('ifthenpay_request', default=False)


class _GatewayLogFilter(logging.Filter):
    """HTTPX logs status query URLs; httpcore debug may contain wire headers."""
    def filter(self, record):
        if _gateway_request.get():
            record.msg = 'IFTHENPAY transport event'
            record.args = ()
            record.exc_info = None
            record.exc_text = None
            record.stack_info = None
        return True


for _name in ('httpx', 'httpcore.connection', 'httpcore.http11', 'httpcore.http2',
              'httpcore.proxy', 'httpcore.socks'):
    logging.getLogger(_name).addFilter(_GatewayLogFilter())


def validate_gateway_base(value: str) -> str:
    # Exact allowlist rejects credentials, alternate ports, queries and path tricks.
    if not isinstance(value, str) or value.strip().rstrip('/') != IFTHENPAY_API_BASE:
        raise ValueError('Endpoint IFTHENPAY inválido. Usa o endereço HTTPS oficial.')
    return IFTHENPAY_API_BASE


def validate_email(value: str) -> str:
    if not isinstance(value, str) or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError('E-mail inválido.')
    value = value.strip()
    if value and (len(value) > 100 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', value)):
        raise ValueError('E-mail inválido.')
    return value


def valid_request_id(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_+=-]{1,128}', value) is not None


def invalid_response() -> HTTPException:
    return HTTPException(status_code=502, detail='Resposta inválida do gateway IFTHENPAY.')


async def gateway_request(api_base: str, method: str, path: str, **kwargs) -> dict:
    try:
        base = validate_gateway_base(api_base)
    except ValueError:
        raise HTTPException(status_code=503, detail='Configuração do gateway IFTHENPAY inválida.') from None
    token = _gateway_request.set(True)
    try:
        # No redirect/retry or environment proxy may forward merchant credentials.
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=False, trust_env=False) as client:
            async with client.stream(method, base + path, **kwargs) as response:
                if not response.is_success:
                    logger.warning('IFTHENPAY HTTP error: status=%d', response.status_code)
                    raise HTTPException(status_code=502, detail='Erro de comunicação com o gateway IFTHENPAY.')
                contents = bytearray()
                async for chunk in response.aiter_bytes():
                    if len(contents) + len(chunk) > MAX_RESPONSE_BYTES:
                        raise invalid_response()
                    contents.extend(chunk)
                try:
                    result = json.loads(contents)
                except (ValueError, UnicodeError):
                    raise invalid_response() from None
                if not isinstance(result, dict):
                    raise invalid_response()
                return result
    except httpx.HTTPError:
        logger.warning('IFTHENPAY communication failed')
        raise HTTPException(status_code=502, detail='Erro de comunicação com o gateway IFTHENPAY.') from None
    finally:
        _gateway_request.reset(token)


def validate_gateway_response(result: dict, *, amount: Decimal | None = None,
                              request_id: str | None = None) -> dict:
    status = result.get('Status')
    message = result.get('Message')
    if not isinstance(status, str) or not re.fullmatch(r'[0-9]{3}', status):
        raise invalid_response()
    if not isinstance(message, str) or len(message) > 300 or any(ord(c) < 32 for c in message):
        raise invalid_response()
    validated = {'Status': status}
    if status == '000':
        # Never expose arbitrary provider text, nor interpret an unknown success message.
        safe_messages = {'pending': 'Pending', 'pendente': 'Pending', 'success': 'Success'}
        safe_message = safe_messages.get(message.strip().lower())
        if safe_message is None or (amount is not None and safe_message != 'Pending'):
            raise invalid_response()
        validated['Message'] = safe_message
    else:
        validated['Message'] = 'Não foi possível processar o pedido MB WAY.'

    response_id = result.get('RequestId')
    if status == '000' or response_id is not None:
        if not valid_request_id(response_id) or (request_id is not None and response_id != request_id):
            raise invalid_response()
        validated['RequestId'] = response_id
    if amount is not None and status == '000':
        raw_amount = result.get('Amount')
        try:
            provider_amount = Decimal(str(raw_amount))
        except (InvalidOperation, ValueError):
            raise invalid_response() from None
        if not provider_amount.is_finite() or provider_amount != amount:
            raise invalid_response()
        validated['Amount'] = float(provider_amount)
    for name in ('CreatedAt', 'UpdateAt'):
        if name in result:
            value = result[name]
            if not isinstance(value, str) or not re.fullmatch(r'[0-9TZ:+. /-]{1,40}', value):
                raise invalid_response()
            validated[name] = value
    return validated
