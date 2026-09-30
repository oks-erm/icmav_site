"""
routers/donations.py — Endpoints assíncronos de pagamentos MB WAY via IFTHENPAY.
"""

import json
import uuid
import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from ..database import get_session
from ..crud import get_setting

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Donations"])


class DonationRequest(BaseModel):
    amount: float = Field(gt=0)
    phone: str
    category: str | None = Field(default=None)
    email: str | None = Field(default=None)
    description: str | None = Field(default=None)


def normalize_phone(phone: str) -> str:
    digits = "".join(c for c in phone if c.isdigit())
    if digits.startswith("351") and len(digits) == 12:
        digits = digits[3:]
    if len(digits) != 9:
        raise ValueError("Número inválido. Usa um número português com 9 dígitos.")
    return f"351#{digits}"


def get_ifthenpay_credentials(session: Session) -> dict:
    for key in ("ifthenpay_config", "sibs_config"):
        setting = get_setting(session, key)
        if setting and setting.value:
            try:
                cfg = json.loads(setting.value)
                if isinstance(cfg, dict):
                    api_base = str(cfg.get("api_base") or cfg.get("sibs_api_base") or "").strip().rstrip("/")
                    mbway_key = str(cfg.get("mbway_key") or cfg.get("sibs_client_id") or "").strip()
                    default_email = str(cfg.get("default_email") or "").strip()
                    if mbway_key or api_base:
                        return {
                            "api_base": api_base or "https://api.ifthenpay.com/spg/payment",
                            "mbway_key": mbway_key,
                            "default_email": default_email,
                        }
            except Exception as exc:
                logger.error("Erro ao ler credenciais IFTHENPAY: %s", exc)

    return {
        "api_base": "https://api.ifthenpay.com/spg/payment",
        "mbway_key": "",
        "default_email": "",
    }


@router.get("/health")
def health():
    return {"ok": True}


@router.post("/donate/mbway")
async def donate_mbway(
    data: DonationRequest,
    session: Session = Depends(get_session)
):
    creds = get_ifthenpay_credentials(session)
    api_base = creds["api_base"]
    mbway_key = creds["mbway_key"]
    default_email = creds["default_email"]

    if not mbway_key:
        raise HTTPException(
            status_code=503,
            detail="A Gateway de pagamentos IFTHENPAY não se encontra configurada. Por favor configura os acessos no painel de administração."
        )

    try:
        customer_phone = normalize_phone(data.phone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # orderId limitado a 15 caracteres conforme API IFTHENPAY
    order_id = f"DON{uuid.uuid4().hex[:12]}"
    category_name = (data.category or "Ofertas").strip()
    tx_description = (data.description or f"Donativo ICMAV - {category_name}").strip()[:100]

    # Email: usa o do doador se preenchido, senão o configurado em Admin
    donor_email = (data.email or "").strip()
    final_email = (donor_email or default_email or "").strip()

    payload = {
        "mbWayKey": mbway_key,
        "orderId": order_id,
        "amount": f"{data.amount:.2f}",
        "mobileNumber": customer_phone,
        "description": tx_description,
    }
    if final_email:
        payload["email"] = final_email[:100]

    endpoint_url = f"{api_base}/mbway"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(endpoint_url, json=payload)
        except Exception as exc:
            logger.error("Erro assíncrono na comunicação com IFTHENPAY: %s", exc)
            raise HTTPException(status_code=502, detail="Erro de comunicação com o gateway IFTHENPAY.")

        if not resp.is_success:
            logger.error("IFTHENPAY erro [%d]: %s", resp.status_code, resp.text)
            raise HTTPException(
                status_code=502,
                detail=f"Resposta de erro do gateway IFTHENPAY [{resp.status_code}]."
            )

        try:
            res_data = resp.json()
        except Exception:
            raise HTTPException(status_code=502, detail="Resposta inválida do gateway IFTHENPAY.")

        status_code = str(res_data.get("Status", ""))
        message = str(res_data.get("Message", ""))

        if status_code != "000":
            logger.warning("IFTHENPAY recusou inicialização: Status=%s, Msg=%s", status_code, message)
            if status_code == "122":
                err_detail = "Transação recusada no MB WAY."
            elif status_code == "100":
                err_detail = "Não foi possível concluir a inicialização. Por favor tenta novamente."
            else:
                err_detail = message or "Não foi possível processar o pedido MB WAY."
            raise HTTPException(status_code=400, detail=err_detail)

    return {
        "ok": True,
        "orderId": order_id,
        "requestId": res_data.get("RequestId"),
        "amount": res_data.get("Amount", data.amount),
        "message": message or "Pending",
        "status": status_code,
    }


@router.get("/payment-status/{request_id}")
async def payment_status(
    request_id: str,
    session: Session = Depends(get_session)
):
    creds = get_ifthenpay_credentials(session)
    api_base = creds["api_base"]
    mbway_key = creds["mbway_key"]

    if not mbway_key:
        raise HTTPException(
            status_code=503,
            detail="A Gateway de pagamentos IFTHENPAY não se encontra configurada."
        )

    endpoint_url = f"{api_base}/mbway/status"
    params = {
        "mbWayKey": mbway_key,
        "requestId": request_id,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(endpoint_url, params=params)
        except Exception as exc:
            logger.error("Erro na consulta de estado IFTHENPAY: %s", exc)
            raise HTTPException(status_code=502, detail="Erro de comunicação ao consultar estado.")

        if not resp.is_success:
            logger.error("IFTHENPAY status erro [%d]: %s", resp.status_code, resp.text)
            raise HTTPException(
                status_code=500,
                detail="Não foi possível consultar o estado do pagamento."
            )

        return resp.json()
