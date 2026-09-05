from sqlmodel import Session, select
from .models import AppSetting


def get_setting(session: Session, key: str):
    statement = select(AppSetting).where(AppSetting.key == key)
    return session.exec(statement).first()


def upsert_setting(session: Session, key: str, value: str):
    setting = get_setting(session, key)

    if setting:
        setting.value = value
    else:
        setting = AppSetting(key=key, value=value)
        session.add(setting)

    session.commit()
    session.refresh(setting)
    return setting