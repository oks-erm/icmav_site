from typing import Optional
from sqlmodel import SQLModel, Field


class AppSetting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str

class PaymentAttempt(SQLModel, table=True):
    """Minimal durable retry ledger; contact details and gateway keys are never stored."""
    key: str = Field(primary_key=True)
    fingerprint: str
    client_fingerprint: str = Field(index=True)
    phone_fingerprint: str = Field(index=True)
    created_at: float = Field(index=True)
    order_id: str
    state: str = 'pending'
    request_id: Optional[str] = None
    response_json: Optional[str] = None
    http_status: int = 200
    last_poll_at: float = 0
    status_json: Optional[str] = None
