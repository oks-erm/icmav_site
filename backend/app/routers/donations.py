"""
routers/donations.py — Endpoints assíncronos de pagamentos MB WAY e estado via SIBS com configurações do Admin.
"""

import json
import uuid
import logging
from datetime import datetime, timezone

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


def normalize_phone(phone: str) -> str:
    digits = "".join(c for c in phone if c.isdigit())
    if digits.startswith("351") and len(digits) == 12:
        digits = digits[3:]
    if len(digits) != 9:
        raise ValueError("Número inválido. Usa um número português com 9 dígitos.")
    return f"351#{digits}"


def get_sibs_credentials(session: Session) -> dict:
    setting = get_setting(session, "sibs_config")
    if setting and setting.value:
        try:
            cfg = json.loads(setting.value)
            if isinstance(cfg, dict):
                return {
                    "sibs_api_base": str(cfg.get("sibs_api_base") or "").strip().rstrip("/"),
                    "sibs_bearer_token": str(cfg.get("sibs_bearer_token") or "").strip(),
                    "sibs_client_id": str(cfg.get("sibs_client_id") or "").strip(),
                    "sibs_client_secret": str(cfg.get("sibs_client_secret") or "").strip(),
                    "sibs_terminal_id": str(cfg.get("sibs_terminal_id") or "").strip(),
                }
        except Exception as exc:
            logger.error("Erro ao ler sibs_config da base de dados: %s", exc)

    return {
        "sibs_api_base": "",
        "sibs_bearer_token": "",
        "sibs_client_id": "",
        "sibs_client_secret": "",
        "sibs_terminal_id": "",
    }


@router.get("/health")
def health():
    return {"ok": True}


@router.post("/donate/mbway")
async def donate_mbway(
    data: DonationRequest,
    session: Session = Depends(get_session)
):
    creds = get_sibs_credentials(session)

    sibs_api_base = creds["sibs_api_base"]
    sibs_bearer_token = creds["sibs_bearer_token"]
    sibs_client_id = creds["sibs_client_id"]
    sibs_terminal_id = creds["sibs_terminal_id"]

    if not sibs_api_base or not sibs_bearer_token or not sibs_client_id:
        raise HTTPException(
            status_code=503,
            detail="A Gateway de pagamentos SIBS não se encontra configurada. Por favor configura os acessos no painel de administração."
        )

    try:
        customer_phone = normalize_phone(data.phone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    merchant_transaction_id = f"donativo-{uuid.uuid4().hex[:12]}"
    current_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    category_name = (data.category or "Ofertas").strip()
    tx_description = f"Donativo ICMAV - {category_name}"

    try:
        terminal_id_num = int(sibs_terminal_id) if sibs_terminal_id else 0
    except ValueError:
        terminal_id_num = 0

    create_payload = {
        "merchant": {
            "terminalId": terminal_id_num,
            "channel": "web",
            "merchantTransactionId": merchant_transaction_id
        },
        "transaction": {
            "transactionTimestamp": current_timestamp,
            "description": tx_description,
            "moto": False,
            "paymentType": "PURS",
            "amount": {
                "value": round(data.amount, 2),
                "currency": "EUR"
            },
            "paymentMethod": ["MBWAY"]
        }
    }

    headers_create = {
        "Authorization": f"Bearer {sibs_bearer_token}",
        "X-IBM-Client-Id": sibs_client_id,
        "Content-Type": "application/json"
    }

    print("\n" + "=" * 65, flush=True)
    print("🚀 [SIBS MB WAY REQUEST INICIADO]", flush=True)
    print(f"📍 Target Endpoint: {sibs_api_base}/payments", flush=True)
    print("📦 Payload /payments gerado:", flush=True)
    print(json.dumps(create_payload, indent=2, ensure_ascii=False), flush=True)
    print("=" * 65 + "\n", flush=True)

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            create_resp = await client.post(
                f"{sibs_api_base}/payments",
                json=create_payload,
                headers=headers_create
            )
        except Exception as exc:
            logger.error("Erro assíncrono na comunicação com SIBS (/payments): %s", exc)
            print(f"❌ Erro de comunicação com SIBS: {exc}", flush=True)
            raise HTTPException(status_code=502, detail="Erro de comunicação com o gateway de pagamentos.")

        print(f"📥 SIBS create_resp [{create_resp.status_code}]: {create_resp.text}", flush=True)

        if not create_resp.is_success:
            logger.error("SIBS create_payment erro [%d]: %s", create_resp.status_code, create_resp.text)
            print("=" * 65 + "\n", flush=True)
            raise HTTPException(
                status_code=500,
                detail=f"Resposta da SIBS [{create_resp.status_code}]: {create_resp.text}"
            )

        create_data = create_resp.json()
        transaction_id = create_data.get("transactionID")
        transaction_signature = create_data.get("transactionSignature")

        if not transaction_id or not transaction_signature:
            logger.error("SIBS não devolveu transactionID ou signature: %s", create_data)
            raise HTTPException(status_code=500, detail="Resposta inválida do gateway de pagamentos.")

        purchase_payload = {
            "customerPhone": customer_phone
        }

        print("\n" + "=" * 65, flush=True)
        print("📱 [SIBS MB WAY PURCHASE PAYLOAD]", flush=True)
        print(f"📍 Target: {sibs_api_base}/payments/{transaction_id}/mbway-id/purchase", flush=True)
        print("📦 Purchase payload gerado:", flush=True)
        print(json.dumps(purchase_payload, indent=2, ensure_ascii=False), flush=True)
        print("=" * 65 + "\n", flush=True)

        headers_purchase = {
            "Authorization": f"Digest {transaction_signature}",
            "X-IBM-Client-Id": sibs_client_id,
            "Content-Type": "application/json"
        }

        try:
            purchase_resp = await client.post(
                f"{sibs_api_base}/payments/{transaction_id}/mbway-id/purchase",
                json=purchase_payload,
                headers=headers_purchase
            )
        except Exception as exc:
            logger.error("Erro assíncrono na comunicação com SIBS (/mbway-id/purchase): %s", exc)
            raise HTTPException(status_code=502, detail="Erro de comunicação ao enviar pedido MB WAY.")

        logger.info("SIBS purchase_resp [%d]: %s", purchase_resp.status_code, purchase_resp.text)

        if not purchase_resp.is_success:
            logger.error("SIBS mbway_purchase erro [%d]: %s", purchase_resp.status_code, purchase_resp.text)
            raise HTTPException(
                status_code=500,
                detail="Não foi possível processar o pedido MB WAY no teu número."
            )

        purchase_data = purchase_resp.json()

    return {
        "ok": True,
        "transactionId": transaction_id,
        "merchantTransactionId": merchant_transaction_id,
        "sibsResponse": purchase_data
    }


@router.get("/payment-status/{transaction_id}")
async def payment_status(
    transaction_id: str,
    session: Session = Depends(get_session)
):
    creds = get_sibs_credentials(session)
    sibs_api_base = creds["sibs_api_base"]
    sibs_bearer_token = creds["sibs_bearer_token"]
    sibs_client_id = creds["sibs_client_id"]

    if not sibs_api_base or not sibs_bearer_token or not sibs_client_id:
        raise HTTPException(
            status_code=503,
            detail="A Gateway de pagamentos SIBS não se encontra configurada."
        )

    headers = {
        "Authorization": f"Bearer {sibs_bearer_token}",
        "X-IBM-Client-Id": sibs_client_id,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(
                f"{sibs_api_base}/payments/{transaction_id}/status",
                headers=headers
            )
        except Exception as exc:
            logger.error("Erro assíncrono na consulta de estado SIBS: %s", exc)
            raise HTTPException(status_code=502, detail="Erro de comunicação ao consultar estado.")

        if not resp.is_success:
            logger.error("SIBS payment_status erro [%d]: %s", resp.status_code, resp.text)
            raise HTTPException(
                status_code=500,
                detail="Não foi possível consultar o estado do pagamento."
            )

        return resp.json()
