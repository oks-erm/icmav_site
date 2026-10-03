"""Authenticated encryption for merchant credentials stored in application settings."""
import json
import os
from cryptography.fernet import Fernet, InvalidToken

SENSITIVE_SETTINGS = frozenset({'ifthenpay_config', 'sibs_config'})
SECRET_FIELDS = frozenset({'mbway_key', 'ifthenpay_mbway_key', 'sibs_client_id', 'sibs_client_secret', 'sibs_bearer_token'})
PREFIX = 'fernet:v1:'


def _cipher():
    try:
        return Fernet(os.environ.get('SETTINGS_ENCRYPTION_KEY', '').encode('ascii'))
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError('A valid SETTINGS_ENCRYPTION_KEY is required for payment credentials.') from None


def encrypt_setting(key: str, value: str) -> str:
    if key not in SENSITIVE_SETTINGS:
        return value
    payload = json.loads(value)
    for field in SECRET_FIELDS:
        secret = payload.get(field)
        if secret:
            # Inputs are always plaintext; never trust a caller-supplied ciphertext prefix.
            payload[field] = PREFIX + _cipher().encrypt(str(secret).encode()).decode('ascii')
    return json.dumps(payload, ensure_ascii=False)


def decrypt_setting(key: str, value: str) -> str:
    if key not in SENSITIVE_SETTINGS:
        return value
    payload = json.loads(value)
    for field in SECRET_FIELDS:
        secret = payload.get(field)
        if secret and str(secret).startswith(PREFIX):
            try:
                payload[field] = _cipher().decrypt(str(secret)[len(PREFIX):].encode('ascii')).decode()
            except (InvalidToken, ValueError, UnicodeError):
                raise RuntimeError('Cannot decrypt payment credentials; restore the original encryption key.') from None
        elif secret:
            raise RuntimeError('Legacy payment credentials must be encrypted before use.')
    return json.dumps(payload, ensure_ascii=False)
