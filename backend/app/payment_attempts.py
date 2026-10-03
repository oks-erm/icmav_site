"""Persist payment reservations before transport; uncertain calls must never be retried."""
import base64
import hashlib
import hmac
import json
import os
import time
import uuid

from fastapi import HTTPException
from sqlalchemy import func, text
from sqlmodel import Session, select

from .models import PaymentAttempt

UNKNOWN_DETAIL = 'Estado do pagamento desconhecido. Verifica a app MB WAY e contacta a tesouraria antes de fazer outro pagamento.'
MAX_ATTEMPTS = 100_000


def validate_attempt_key(key: str | None) -> str:
    try:
        parsed = uuid.UUID(key or '')
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(400, 'É necessário um Idempotency-Key UUID aleatório válido.') from None
    if parsed.version != 4 or str(parsed) != key:
        raise HTTPException(400, 'É necessário um Idempotency-Key UUID aleatório válido.')
    return key


def _fingerprint(context: str, value: str) -> str:
    try:
        key = base64.urlsafe_b64decode(os.environ.get('SETTINGS_ENCRYPTION_KEY', '').encode('ascii'))
    except (ValueError, UnicodeError):
        raise HTTPException(503, 'Configuração de segurança dos pagamentos inválida.') from None
    if len(key) != 32:
        raise HTTPException(503, 'Configuração de segurança dos pagamentos inválida.')
    return hmac.new(key, (context + '\0' + value).encode(), hashlib.sha256).hexdigest()


def attempt_result(attempt: PaymentAttempt) -> dict:
    if attempt.state not in {'ready', 'declined'} or not attempt.response_json:
        raise HTTPException(409, UNKNOWN_DETAIL)
    result = json.loads(attempt.response_json)
    if attempt.http_status != 200:
        raise HTTPException(attempt.http_status, result['detail'])
    return result


def reserve_attempt(session: Session, key: str, payload: dict, client: str) -> tuple[PaymentAttempt, bool]:
    key = validate_attempt_key(key)
    # orderId is generated only for the winning reservation and never affects retries.
    fingerprint = _fingerprint('payment-input', json.dumps(
        {name: value for name, value in payload.items() if name != 'orderId'}, sort_keys=True, separators=(',', ':')))
    client_hash = _fingerprint('payment-client', client)
    phone_hash = _fingerprint('payment-phone', payload['mobileNumber'])
    now = time.time()
    with Session(session.get_bind(), expire_on_commit=False) as ledger:
        # SQLite's write reservation serializes both the rate checks and key claim.
        ledger.exec(text('BEGIN IMMEDIATE'))
        existing = ledger.get(PaymentAttempt, key)
        if existing:
            if not hmac.compare_digest(existing.fingerprint, fingerprint):
                raise HTTPException(409, 'Este pedido já foi usado com outros dados.')
            attempt_result(existing)  # Pending/uncertain attempts are never reclaimed.
            return existing, False
        recent = select(func.count()).select_from(PaymentAttempt).where(PaymentAttempt.created_at > now - 300)
        limits = (
            (recent.where(PaymentAttempt.phone_fingerprint == phone_hash), 3),
            (recent.where(PaymentAttempt.client_fingerprint == client_hash), 10),
            (recent, 100),
        )
        if any(ledger.exec(query).one() >= limit for query, limit in limits):
            raise HTTPException(429, 'Demasiados pedidos de pagamento. Aguarda antes de tentar novamente.', headers={'Retry-After': '300'})
        # Retain claims indefinitely: deleting one would make an old key chargeable again.
        if ledger.exec(select(func.count()).select_from(PaymentAttempt)).one() >= MAX_ATTEMPTS:
            raise HTTPException(503, 'Pagamentos temporariamente indisponíveis. Contacta a tesouraria.')
        attempt = PaymentAttempt(key=key, fingerprint=fingerprint, client_fingerprint=client_hash,
                                 phone_fingerprint=phone_hash, created_at=now, order_id='DON' + uuid.uuid4().hex[:12])
        ledger.add(attempt)
        ledger.commit()
        return attempt, True


def finish_attempt(session: Session, key: str, state: str, result: dict | None = None, http_status: int = 200):
    with Session(session.get_bind()) as ledger:
        attempt = ledger.get(PaymentAttempt, key)
        if attempt is None:
            raise RuntimeError('Payment reservation is missing.')
        attempt.state = state
        attempt.http_status = http_status
        attempt.response_json = json.dumps(result) if result is not None else None
        attempt.request_id = result.get('requestId') if result else None
        ledger.add(attempt)
        ledger.commit()


def recover_attempt(session: Session, key: str) -> dict:
    key = validate_attempt_key(key)
    attempt = session.get(PaymentAttempt, key)
    if attempt is None:
        raise HTTPException(404, 'Pedido não encontrado. Confirma o estado junto da tesouraria antes de repetir.')
    return attempt_result(attempt)


def claim_status_poll(session: Session, key: str, request_id: str) -> dict | None:
    key = validate_attempt_key(key)
    with Session(session.get_bind()) as ledger:
        ledger.exec(text('BEGIN IMMEDIATE'))
        attempt = ledger.get(PaymentAttempt, key)
        if not attempt or attempt.request_id != request_id:
            raise HTTPException(404, 'Pedido de pagamento não encontrado.')
        now = time.time()
        cached = json.loads(attempt.status_json) if attempt.status_json else None
        if cached and cached.get('Status') == '000' and cached.get('Message') == 'Success':
            return cached
        if now - attempt.last_poll_at < 3:
            if cached:
                return cached
            raise HTTPException(429, 'Aguarda antes de consultar novamente.', headers={'Retry-After': '3'})
        attempt.last_poll_at = now
        ledger.add(attempt)
        ledger.commit()
    return None


def save_status(session: Session, key: str, result: dict) -> dict:
    with Session(session.get_bind()) as ledger:
        # A slow older poll may finish after a newer confirmation. Success is final.
        ledger.exec(text('BEGIN IMMEDIATE'))
        attempt = ledger.get(PaymentAttempt, key)
        previous = json.loads(attempt.status_json) if attempt.status_json else None
        if previous and previous.get('Status') == '000' and previous.get('Message') == 'Success':
            return previous
        attempt.status_json = json.dumps(result)
        ledger.add(attempt)
        ledger.commit()
    return result


def attempt_was_started(session: Session, key: str | None) -> bool:
    """Only an absent durable claim permits an explicit 'not sent' response."""
    if not isinstance(key, str) or len(key) > 36:
        return False
    with Session(session.get_bind()) as ledger:
        return ledger.get(PaymentAttempt, key) is not None
