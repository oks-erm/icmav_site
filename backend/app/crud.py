from sqlmodel import Session, select
from .models import AppSetting
from .secret_storage import decrypt_setting, encrypt_setting, SENSITIVE_SETTINGS, SECRET_FIELDS, PREFIX
import json


def _get_record(session: Session, key: str):
    return session.exec(select(AppSetting).where(AppSetting.key == key)).first()


def _snapshot(setting: AppSetting):
    # Keep plaintext out of the identity map so unrelated commits cannot persist it.
    return AppSetting(id=setting.id, key=setting.key, value=decrypt_setting(setting.key, setting.value))


def get_setting(session: Session, key: str):
    setting = _get_record(session, key)
    return _snapshot(setting) if setting else None


def upsert_setting(session: Session, key: str, value: str):
    stored_value = encrypt_setting(key, value)
    setting = _get_record(session, key)
    if setting:
        setting.value = stored_value
    else:
        setting = AppSetting(key=key, value=stored_value)
        session.add(setting)
    session.commit()
    session.refresh(setting)
    return _snapshot(setting)


def migrate_secret_settings(session: Session):
    """Encrypt legacy fields in one transaction, preserving all other settings."""
    records = session.exec(select(AppSetting).where(AppSetting.key.in_(SENSITIVE_SETTINGS))).all()
    for setting in records:
        payload = json.loads(setting.value)
        changed = False
        for field in SECRET_FIELDS:
            secret = payload.get(field)
            if secret and not str(secret).startswith(PREFIX):
                encrypted = json.loads(encrypt_setting(setting.key, json.dumps({field: secret})))
                payload[field] = encrypted[field]
                changed = True
        # Also fail closed if the stored ciphertext cannot be recovered with this key.
        value = json.dumps(payload, ensure_ascii=False)
        decrypt_setting(setting.key, value)
        if changed:
            setting.value = value
    session.commit()
