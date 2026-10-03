"""
validators.py — Funções de validação de schemas dinâmicos e manipulação de uploads.
"""

import io
import uuid
import warnings
from typing import Any
from pathlib import Path
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from .defaults import MAP_CENTER_LAT_OFFSET, MAP_CENTER_LNG_OFFSET
from .gateway import IFTHENPAY_API_BASE, validate_gateway_base, validate_email

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_IMAGE_FORMATS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
}
ALLOWED_VIDEO_FORMATS = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
}
MAX_VIDEO_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB


async def save_and_validate_media(file: UploadFile, target_dir: Path) -> dict:
    """Valida e guarda ficheiro multimédia (imagem até 5MB ou vídeo até 50MB)."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Ficheiro inválido")

    filename_lower = file.filename.lower()

    # Verificar se é vídeo
    matched_video_ext = next((ext for ext in ALLOWED_VIDEO_FORMATS if filename_lower.endswith(ext)), None)
    limit = MAX_VIDEO_UPLOAD_SIZE if matched_video_ext else MAX_UPLOAD_SIZE
    contents = await file.read(limit + 1)
    if matched_video_ext:
        if len(contents) > MAX_VIDEO_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Vídeo demasiado grande. Limite máximo: {MAX_VIDEO_UPLOAD_SIZE // (1024 * 1024)}MB"
            )
        if not _valid_video_header(contents, matched_video_ext):
            raise HTTPException(status_code=400, detail="O ficheiro enviado não é um vídeo MP4 ou WEBM válido.")
        filename = f"{uuid.uuid4().hex}{matched_video_ext}"
        destination = target_dir / filename
        destination.write_bytes(contents)
        return {"mediaType": "video", "filename": filename}

    # Se não for vídeo, valida como imagem
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Ficheiro demasiado grande. Limite máximo: {MAX_UPLOAD_SIZE // (1024 * 1024)}MB"
        )

    try:
        image_format = _verified_image_format(contents)
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(
            status_code=400,
            detail="Ficheiro inválido. Envia uma imagem (JPG, PNG, WEBP) ou vídeo (MP4, WEBM)."
        )

    extension = ALLOWED_IMAGE_FORMATS.get(image_format or "")
    if not extension:
        raise HTTPException(
            status_code=400,
            detail="Formato não suportado. Usa JPG, PNG, WEBP, MP4 ou WEBM."
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    destination = target_dir / filename
    destination.write_bytes(contents)
    return {"mediaType": "image", "filename": filename}


async def save_and_validate_image(file: UploadFile, target_dir: Path) -> str:
    """Valida o ficheiro com Pillow (magic bytes e integridade) e tamanho máximo antes de guardar."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Ficheiro inválido")

    contents = await file.read(MAX_UPLOAD_SIZE + 1)

    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Ficheiro demasiado grande. Limite máximo: {MAX_UPLOAD_SIZE // (1024 * 1024)}MB"
        )

    try:
        image_format = _verified_image_format(contents)
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(
            status_code=400,
            detail="O ficheiro enviado não é uma imagem válida (JPG, PNG ou WEBP)."
        )

    extension = ALLOWED_IMAGE_FORMATS.get(image_format or "")
    if not extension:
        raise HTTPException(
            status_code=400,
            detail="Formato de imagem não suportado. Usa JPG, PNG ou WEBP."
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    destination = target_dir / filename
    destination.write_bytes(contents)
    return filename


def _verified_image_format(contents: bytes) -> str | None:
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(contents)) as image:
            image.verify()
            return image.format


def _valid_video_header(contents: bytes, extension: str) -> bool:
    """Check container identity; full codec validation requires a media scanner."""
    if extension == '.mp4':
        if len(contents) < 24 or contents[4:8] != b'ftyp':
            return False
        box_size = int.from_bytes(contents[:4], 'big')
        if box_size < 16 or box_size > len(contents) or box_size % 4:
            return False
        brands = [contents[8:12]] + [contents[i:i + 4] for i in range(16, box_size, 4)]
        return bool(set(brands) & {b'isom', b'iso2', b'mp41', b'mp42', b'avc1', b'M4V ', b'dash'})
    # EBML header and WebM DocType element (not merely an arbitrary .webm suffix).
    return contents.startswith(b'\x1a\x45\xdf\xa3') and b'\x42\x82\x84webm' in contents[:4096]


# ─── PURPOSES VALIDATOR ──────────────────────────────────────────────────────

def validate_purposes(payload: Any) -> list[dict]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    required_fields = {
        "title", "icon", "bgClass", "desc", "biblicalPassage", "biblicalReference"
    }

    for item in payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=400, detail="Cada item deve ser um objeto")

        missing = required_fields - set(item.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Campos em falta: {', '.join(sorted(missing))}"
            )

    return payload


# ─── PASTORAL TEAM VALIDATOR ──────────────────────────────────────────────────

def validate_pastoral_team(payload: Any) -> list[dict]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    required_fields = {
        "id", "name", "photo", "bio", "spouseId", "isLeadPair"
    }

    seen_ids = set()

    for item in payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=400, detail="Cada item deve ser um objeto")

        missing = required_fields - set(item.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Campos em falta: {', '.join(sorted(missing))}"
            )

        if not isinstance(item["id"], int):
            raise HTTPException(status_code=400, detail="Cada id deve ser um inteiro")

        if item["id"] in seen_ids:
            raise HTTPException(status_code=400, detail="Existem ids duplicados")

        seen_ids.add(item["id"])

        for str_field in ["name", "photo", "bio"]:
            if not isinstance(item[str_field], str):
                raise HTTPException(status_code=400, detail=f"O campo {str_field} deve ser texto")

        if item["spouseId"] is not None and not isinstance(item["spouseId"], int):
            raise HTTPException(status_code=400, detail="O campo spouseId deve ser inteiro ou null")

        if not isinstance(item["isLeadPair"], bool):
            raise HTTPException(status_code=400, detail="O campo isLeadPair deve ser boolean")

    return payload


# ─── MINISTRIES VALIDATOR ─────────────────────────────────────────────────────

def validate_ministries(payload: Any) -> list[dict]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    required_fields = {"name", "slug", "icon", "bgClass", "desc"}
    validated_items: list[dict] = []

    for item in payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=400, detail="Cada item deve ser um objeto")

        missing = required_fields - set(item.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Campos em falta: {', '.join(sorted(missing))}"
            )

        # Campos obrigatórios base
        norm_item = {
            "name": str(item["name"]).strip(),
            "slug": str(item["slug"]).strip(),
            "icon": str(item["icon"]).strip(),
            "bgClass": str(item["bgClass"]).strip(),
            "desc": str(item["desc"]).strip(),
        }

        # Campos opcionais ricos de detalhe
        if "longDescription" in item:
            if isinstance(item["longDescription"], list):
                norm_item["longDescription"] = [str(p).strip() for p in item["longDescription"] if str(p).strip()]
            elif isinstance(item["longDescription"], str):
                # Se for string com quebras de linha, converte para lista de parágrafos
                norm_item["longDescription"] = [p.strip() for p in item["longDescription"].split("\n\n") if p.strip()]

        if "leader" in item:
            norm_item["leader"] = str(item["leader"]).strip()

        if "leaderPhoto" in item:
            norm_item["leaderPhoto"] = str(item["leaderPhoto"]).strip()

        if "contact" in item:
            norm_item["contact"] = str(item["contact"]).strip()

        if "media" in item and isinstance(item["media"], dict):
            norm_item["media"] = {
                "type": item["media"].get("type", "image"),
                "src": item["media"].get("src", ""),
                "placeholder": item["media"].get("placeholder", ""),
            }

        if "socialMedia" in item and isinstance(item["socialMedia"], list):
            norm_item["socialMedia"] = [
                {
                    "icon": str(s.get("icon", "fab fa-instagram")).strip(),
                    "link": str(s.get("link", "")).strip()
                }
                for s in item["socialMedia"]
                if isinstance(s, dict) and s.get("link")
            ]

        validated_items.append(norm_item)

    return validated_items


# ─── LOCAL GATHERINGS VALIDATORS ──────────────────────────────────────────────

def validate_local_gatherings_content(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="O valor deve ser um objeto")

    required_fields = {"localGatheringsQuote", "localGatheringsQuoteReference", "localGatheringsBody"}
    missing = required_fields - set(payload.keys())
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Campos em falta: {', '.join(sorted(missing))}"
        )

    normalized = {}
    for field in ["localGatheringsQuote", "localGatheringsQuoteReference", "localGatheringsBody"]:
        if not isinstance(payload[field], str) or not payload[field].strip():
            raise HTTPException(
                status_code=400,
                detail=f"O campo {field} deve ser texto válido"
            )
        normalized[field] = payload[field].strip()

    return normalized


def validate_local_gathering_options(payload: Any) -> list[dict]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    required_fields = {"slug", "leaderName", "emailContact", "characteristicTag", "location"}
    validated_items: list[dict] = []

    for item in payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=400, detail="Cada item deve ser um objeto")

        missing = required_fields - set(item.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Campos em falta: {', '.join(sorted(missing))}"
            )

        normalized_item = {}
        for field in ["slug", "leaderName", "emailContact", "characteristicTag", "location"]:
            if not isinstance(item[field], str) or not item[field].strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"O campo {field} deve ser texto válido"
                )
            normalized_item[field] = item[field].strip()

        validated_items.append(normalized_item)

    return validated_items


# ─── GALLERY VALIDATOR ────────────────────────────────────────────────────────

def validate_gallery(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    for item in payload:
        if not isinstance(item, str) or not item.strip():
            raise HTTPException(status_code=400, detail="Cada item deve ser um caminho válido de imagem")

    return payload


# ─── SOCIAL MEDIA VALIDATOR ───────────────────────────────────────────────────

def validate_social_media(payload: Any) -> list[dict]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    required_fields = {"icon", "link", "hoverColor"}

    for item in payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=400, detail="Cada item deve ser um objeto")

        missing = required_fields - set(item.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Campos em falta: {', '.join(sorted(missing))}"
            )

        for field in ["icon", "link", "hoverColor"]:
            if not isinstance(item[field], str) or not item[field].strip():
                raise HTTPException(status_code=400, detail=f"O campo {field} deve ser texto válido")

    return payload


# ─── DONATIONS VALIDATOR ──────────────────────────────────────────────────────

def validate_donations_content(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="O valor deve ser um objeto")

    # Suporta tanto donationsQuoteAuthor como donationsQuoteReference para total compatibilidade
    author_val = payload.get("donationsQuoteAuthor") or payload.get("donationsQuoteReference")
    body_val = payload.get("donationsBody")
    quote_val = payload.get("donationsQuote")

    if not body_val or not isinstance(body_val, str) or not body_val.strip():
        raise HTTPException(status_code=400, detail="O campo donationsBody é obrigatório e deve ser texto válido")
    if not quote_val or not isinstance(quote_val, str) or not quote_val.strip():
        raise HTTPException(status_code=400, detail="O campo donationsQuote é obrigatório e deve ser texto válido")
    if not author_val or not isinstance(author_val, str) or not author_val.strip():
        raise HTTPException(status_code=400, detail="O campo donationsQuoteAuthor é obrigatório e deve ser texto válido")

    # Campos bancários opcionais com defaults seguros
    beneficiary = str(payload.get("beneficiary") or "Igreja Cristã Manancial de Águas Vivas").strip()
    iban = str(payload.get("iban") or "PT50 0007 0246 0014 0750 0033 4").strip()
    bank = str(payload.get("bank") or "NOVO BANCO, SA").strip()
    bic = str(payload.get("bic") or "BESCPTPLXXX").strip()
    treasury_email = str(payload.get("treasuryEmail") or "tesouraria.icmav@gmail.com").strip()

    # Categorias
    raw_categories = payload.get("categories")
    categories_list = []
    if isinstance(raw_categories, list):
        for cat in raw_categories:
            if isinstance(cat, dict) and "name" in cat and str(cat["name"]).strip():
                cat_name = str(cat["name"]).strip()
                cat_id = str(cat.get("id") or cat_name).strip()
                categories_list.append({"id": cat_id, "name": cat_name})
            elif isinstance(cat, str) and cat.strip():
                categories_list.append({"id": cat.strip(), "name": cat.strip()})

    if not categories_list:
        categories_list = [
            {"id": "Ofertas", "name": "Ofertas"},
            {"id": "Dízimos", "name": "Dízimos"},
            {"id": "Missões", "name": "Missões"},
        ]

    return {
        "donationsBody": body_val.strip(),
        "donationsQuote": quote_val.strip(),
        "donationsQuoteAuthor": author_val.strip(),
        "beneficiary": beneficiary,
        "iban": iban,
        "bank": bank,
        "bic": bic,
        "treasuryEmail": treasury_email,
        "categories": categories_list,
    }


# ─── LOCATIONS VALIDATORS ─────────────────────────────────────────────────────

def parse_coordinate_pair(value: str, field_name: str) -> tuple[float, float]:
    parts = value.split(",")
    if len(parts) != 2:
        raise HTTPException(
            status_code=400,
            detail=f"O campo {field_name} deve ter o formato latitude,longitude"
        )

    try:
        lat = float(parts[0].strip())
        lng = float(parts[1].strip())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"O campo {field_name} deve conter coordenadas válidas"
        )

    if not (-90 <= lat <= 90):
        raise HTTPException(status_code=400, detail=f"A latitude de {field_name} é inválida")
    if not (-180 <= lng <= 180):
        raise HTTPException(status_code=400, detail=f"A longitude de {field_name} é inválida")

    return lat, lng


def calculate_map_center_from_marker(marker_position: str) -> str:
    lat, lng = parse_coordinate_pair(marker_position, "markerPosition")
    center_lat = lat + MAP_CENTER_LAT_OFFSET
    center_lng = lng + MAP_CENTER_LNG_OFFSET
    return f"{center_lat:.6f},{center_lng:.6f}"


def validate_locations(payload: Any) -> list[dict]:
    if not isinstance(payload, list):
        raise HTTPException(status_code=400, detail="O valor deve ser uma lista")

    required_fields = {
        "slug", "name", "type", "email", "phone", "address",
        "mapsLink", "customWebsite", "sundayService", "markerPosition", "mapZoom",
    }

    validated_items: list[dict] = []

    for item in payload:
        if not isinstance(item, dict):
            raise HTTPException(status_code=400, detail="Cada item deve ser um objeto")

        missing = required_fields - set(item.keys())
        if missing:
            raise HTTPException(
                status_code=400,
                detail=f"Campos em falta: {', '.join(sorted(missing))}"
            )

        for field in [
            "slug", "name", "type", "email", "phone", "address",
            "mapsLink", "sundayService", "markerPosition",
        ]:
            if not isinstance(item[field], str) or not item[field].strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"O campo {field} deve ser texto válido"
                )

        if item["customWebsite"] is not None and not isinstance(item["customWebsite"], str):
            raise HTTPException(status_code=400, detail="O campo customWebsite deve ser texto ou null")

        if not isinstance(item["mapZoom"], int) or item["mapZoom"] < 1 or item["mapZoom"] > 21:
            raise HTTPException(status_code=400, detail="O campo mapZoom deve estar entre 1 e 21")

        parse_coordinate_pair(item["markerPosition"], "markerPosition")

        normalized_item = {
            "slug": item["slug"].strip(),
            "name": item["name"].strip(),
            "type": item["type"].strip(),
            "email": item["email"].strip(),
            "phone": item["phone"].strip(),
            "address": item["address"].strip(),
            "mapsLink": item["mapsLink"].strip(),
            "customWebsite": item["customWebsite"].strip() if isinstance(item["customWebsite"], str) else None,
            "sundayService": item["sundayService"].strip(),
            "markerPosition": item["markerPosition"].strip(),
            "mapZoom": item["mapZoom"],
            "mapCenter": calculate_map_center_from_marker(item["markerPosition"]),
        }
        validated_items.append(normalized_item)

    return validated_items


# ─── IFTHENPAY CONFIG VALIDATOR ──────────────────────────────────────────────

def validate_ifthenpay_config(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="O valor deve ser um objeto")

    try:
        api_base = validate_gateway_base(payload.get("api_base") or payload.get("sibs_api_base") or IFTHENPAY_API_BASE)
        default_email = validate_email(payload.get("default_email") or payload.get("ifthenpay_default_email") or "")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None

    mbway_key = payload.get("mbway_key") or payload.get("ifthenpay_mbway_key") or payload.get("sibs_client_id") or ""
    if not isinstance(mbway_key, str) or len(mbway_key) > 256 or any(ord(c) < 32 or ord(c) == 127 for c in mbway_key):
        raise HTTPException(status_code=400, detail="Chave MB WAY inválida.")
    mbway_key = mbway_key.strip()

    return {
        "api_base": api_base,
        "mbway_key": mbway_key,
        "default_email": default_email,
    }


def validate_sibs_config(payload: Any) -> dict:
    return validate_ifthenpay_config(payload)


def validate_google_maps_config(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="O valor deve ser um objeto")

    api_key = str(payload.get("apiKey") or payload.get("api_key") or "").strip()
    map_id = str(payload.get("mapId") or payload.get("map_id") or "").strip()

    return {
        "apiKey": api_key,
        "mapId": map_id,
    }
