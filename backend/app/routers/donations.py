"""
routers/donations.py — Endpoints assíncronos de pagamentos MB WAY via IFTHENPAY.
"""

import json
import logging
import re
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Request, Header
from pydantic import BaseModel, Field, field_validator
from sqlmodel import Session

from ..database import get_session
from ..crud import get_setting
from ..gateway import (IFTHENPAY_API_BASE, gateway_request, validate_email,
                       validate_gateway_response, valid_request_id)
from ..validators import validate_ifthenpay_config
from ..payment_attempts import (reserve_attempt, finish_attempt, attempt_result,
                                recover_attempt, validate_attempt_key, claim_status_poll, save_status, attempt_was_started)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Donations"])


def normalize_phone(phone: str) -> str:
    if not re.fullmatch(r'\+?[0-9 ()-]{9,24}', phone):
        raise ValueError("Número inválido. Usa um número português com 9 dígitos.")
    digits = ''.join(c for c in phone if c in '0123456789')
    if digits.startswith('351') and len(digits) == 12:
        digits = digits[3:]
    if len(digits) != 9:
        raise ValueError("Número inválido. Usa um número português com 9 dígitos.")
    return f'351#{digits}'


class DonationRequest(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=9, decimal_places=2, allow_inf_nan=False)
    phone: str = Field(min_length=9, max_length=24)
    category: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=100)

    @field_validator('phone')
    @classmethod
    def check_phone(cls, value):
        normalize_phone(value)
        return value

    @field_validator('email')
    @classmethod
    def check_email(cls, value):
        return validate_email(value) if value is not None else None

    @field_validator('category', 'description')
    @classmethod
    def check_text(cls, value):
        if value is not None and any(ord(c) < 32 or ord(c) == 127 for c in value):
            raise ValueError('Texto inválido.')
        return value.strip() if value is not None else None


def get_ifthenpay_credentials(session: Session) -> dict:
    for key in ('ifthenpay_config', 'sibs_config'):
        setting = get_setting(session, key)
        if setting and setting.value:
            try:
                cfg = json.loads(setting.value)
                # Revalidate persisted/legacy values before any network request.
                credentials = validate_ifthenpay_config(cfg)
            except (ValueError, TypeError, HTTPException):
                logger.warning('Invalid IFTHENPAY configuration')
                raise HTTPException(status_code=503, detail='Configuração do gateway IFTHENPAY inválida.') from None
            if credentials['mbway_key'] or cfg.get('api_base') or cfg.get('sibs_api_base'):
                return credentials
    return {'api_base': IFTHENPAY_API_BASE, 'mbway_key': '', 'default_email': ''}


@router.get('/health')
def health():
    return {'ok': True}


@router.post('/donate/mbway')
async def donate_mbway(data: DonationRequest, request: Request, session: Session = Depends(get_session),
                       idempotency_key: str | None = Header(default=None)):
    try:
        validate_attempt_key(idempotency_key)
        creds = get_ifthenpay_credentials(session)
        if not creds['mbway_key']:
            raise HTTPException(status_code=503, detail='A Gateway de pagamentos IFTHENPAY não se encontra configurada.')
        customer_phone = normalize_phone(data.phone)
        category_name = data.category or 'Ofertas'
        description = (data.description or f'Donativo ICMAV {category_name}')[:100]
        final_email = data.email or creds['default_email']
        payload = {
            'mbWayKey': creds['mbway_key'],
            'amount': f'{data.amount:.2f}', 'mobileNumber': customer_phone,
            'description': description,
        }
        if final_email:
            payload['email'] = final_email
        attempt, is_new = reserve_attempt(session, idempotency_key, {**payload, '_category': data.category},
                                          request.client.host if request.client else 'unknown')
    except HTTPException as exc:
        if not attempt_was_started(session, idempotency_key):
            exc.headers = {**(exc.headers or {}), 'X-Payment-Attempt-State': 'not-sent'}
        raise
    if not is_new:
        return attempt_result(attempt)
    payload['orderId'] = attempt.order_id
    try:
        result = validate_gateway_response(
            await gateway_request(creds['api_base'], 'POST', '/mbway', json=payload), amount=data.amount)
    except HTTPException:
        finish_attempt(session, idempotency_key, 'unknown')
        raise
    # Unexpected errors/cancellation leave the committed pending reservation in place.
    if result['Status'] != '000':
        logger.warning('IFTHENPAY initialization declined: status=%s', result['Status'])
        detail = {
            '122': 'Transação recusada no MB WAY.',
            '100': 'Não foi possível concluir a inicialização. Por favor tenta novamente.',
        }.get(result['Status'], 'Não foi possível processar o pedido MB WAY.')
        finish_attempt(session, idempotency_key, 'declined', {'detail': detail}, 400)
        raise HTTPException(status_code=400, detail=detail)
    response = {
        'ok': True, 'orderId': attempt.order_id, 'requestId': result['RequestId'],
        'amount': result['Amount'], 'message': result['Message'], 'status': result['Status'],
    }

    finish_attempt(session, idempotency_key, 'ready', response)
    return response


@router.get('/donate/attempt')
def donation_attempt(session: Session = Depends(get_session), idempotency_key: str | None = Header(default=None)):
    return recover_attempt(session, idempotency_key)


@router.get('/payment-status/{request_id}')
async def payment_status(request_id: str, session: Session = Depends(get_session),
                         idempotency_key: str | None = Header(default=None)):
    if not valid_request_id(request_id):
        raise HTTPException(status_code=400, detail='Identificador de pagamento inválido.')
    cached = claim_status_poll(session, idempotency_key, request_id)
    if cached is not None:
        return cached
    creds = get_ifthenpay_credentials(session)
    if not creds['mbway_key']:
        raise HTTPException(status_code=503, detail='A Gateway de pagamentos IFTHENPAY não se encontra configurada.')
    result = await gateway_request(creds['api_base'], 'GET', '/mbway/status',
                                   params={'mbWayKey': creds['mbway_key'], 'requestId': request_id})
    validated = validate_gateway_response(result, request_id=request_id)
    return save_status(session, idempotency_key, validated)
