"""
routers/settings.py — Endpoints para gestão de conteúdo de todas as secções do site.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session

from ..database import get_session
from ..crud import get_setting, upsert_setting
from ..schemas import SettingUpdate
from ..auth import get_current_admin
from ..defaults import (
    PASTORAL_TEAM_UPLOADS_DIR,
    GALLERY_UPLOADS_DIR,
    MINISTRIES_UPLOADS_DIR,
    DEFAULT_WELCOME_CONTENT,
    DEFAULT_PURPOSES_CONTENT,
    DEFAULT_PASTORAL_TEAM_CONTENT,
    DEFAULT_MESSAGE_CONTENT,
    DEFAULT_MINISTRIES_PRESENTATION_CONTENT,
    DEFAULT_SERVICES_BANNER_CONTENT,
    DEFAULT_LOCAL_GATHERINGS_CONTENT,
    DEFAULT_LOCAL_GATHERING_OPTIONS,
    DEFAULT_GALLERY_CONTENT,
    DEFAULT_SOCIAL_MEDIA_CONTENT,
    DEFAULT_DONATIONS_CONTENT,
    DEFAULT_LOCATIONS_CONTENT,
    DEFAULT_IFTHENPAY_CONFIG,
    DEFAULT_SIBS_CONFIG,
    DEFAULT_GOOGLE_MAPS_CONFIG,
)
from ..validators import (
    save_and_validate_image,
    save_and_validate_media,
    validate_purposes,
    validate_pastoral_team,
    validate_ministries,
    validate_local_gatherings_content,
    validate_local_gathering_options,
    validate_gallery,
    validate_social_media,
    validate_donations_content,
    validate_locations,
    validate_ifthenpay_config,
    validate_sibs_config,
    validate_google_maps_config,
)

router = APIRouter(prefix="/api/settings", tags=["Settings"])


# ─── 1. WELCOME ───────────────────────────────────────────────────────────────

@router.get("/welcome")
def read_welcome(session: Session = Depends(get_session)):
    setting = get_setting(session, "welcome_content")
    if not setting:
        setting = upsert_setting(session, "welcome_content", DEFAULT_WELCOME_CONTENT)
    return {"key": "welcome_content", "value": setting.value}


@router.put("/welcome")
def update_welcome(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(session, "welcome_content", payload.value)
    return {"success": True, "key": setting.key, "value": setting.value}


@router.post("/welcome/reset")
def reset_welcome(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(session, "welcome_content", DEFAULT_WELCOME_CONTENT)
    return {"success": True, "key": setting.key, "value": setting.value}


# ─── 2. PURPOSES ─────────────────────────────────────────────────────────────

@router.get("/purposes")
def read_purposes(session: Session = Depends(get_session)):
    setting = get_setting(session, "purposes_content")
    if not setting:
        setting = upsert_setting(
            session,
            "purposes_content",
            json.dumps(DEFAULT_PURPOSES_CONTENT, ensure_ascii=False)
        )
    return {"key": "purposes_content", "value": json.loads(setting.value)}


@router.put("/purposes")
def update_purposes(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_purposes(parsed)
    setting = upsert_setting(session, "purposes_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/purposes/reset")
def reset_purposes(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "purposes_content",
        json.dumps(DEFAULT_PURPOSES_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_PURPOSES_CONTENT}


# ─── 3. PASTORAL TEAM ────────────────────────────────────────────────────────

@router.get("/pastoral-team")
def read_pastoral_team(session: Session = Depends(get_session)):
    setting = get_setting(session, "pastoral_team_content")
    if not setting:
        setting = upsert_setting(
            session,
            "pastoral_team_content",
            json.dumps(DEFAULT_PASTORAL_TEAM_CONTENT, ensure_ascii=False)
        )
    return {"key": "pastoral_team_content", "value": json.loads(setting.value)}


@router.put("/pastoral-team")
def update_pastoral_team(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_pastoral_team(parsed)
    setting = upsert_setting(session, "pastoral_team_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/pastoral-team/reset")
def reset_pastoral_team(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "pastoral_team_content",
        json.dumps(DEFAULT_PASTORAL_TEAM_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_PASTORAL_TEAM_CONTENT}


@router.post("/pastoral-team/upload-photo")
async def upload_pastoral_team_photo(
    file: UploadFile = File(...),
    _: str = Depends(get_current_admin),
):
    filename = await save_and_validate_image(file, PASTORAL_TEAM_UPLOADS_DIR)
    return {"success": True, "filename": filename, "url": f"/uploads/pastoral_team/{filename}"}


# ─── 4. MESSAGE ──────────────────────────────────────────────────────────────

@router.get("/message")
def read_message(session: Session = Depends(get_session)):
    setting = get_setting(session, "message_content")
    if not setting:
        setting = upsert_setting(session, "message_content", DEFAULT_MESSAGE_CONTENT)
    return {"key": "message_content", "value": setting.value}


@router.put("/message")
def update_message(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(session, "message_content", payload.value)
    return {"success": True, "key": setting.key, "value": setting.value}


@router.post("/message/reset")
def reset_message(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(session, "message_content", DEFAULT_MESSAGE_CONTENT)
    return {"success": True, "key": setting.key, "value": setting.value}


# ─── 5. MINISTRIES PRESENTATION ─────────────────────────────────────────────

@router.get("/ministries-presentation")
def read_ministries_presentation(session: Session = Depends(get_session)):
    setting = get_setting(session, "ministries_presentation_content")
    if not setting:
        setting = upsert_setting(
            session,
            "ministries_presentation_content",
            json.dumps(DEFAULT_MINISTRIES_PRESENTATION_CONTENT, ensure_ascii=False)
        )
    return {"key": "ministries_presentation_content", "value": json.loads(setting.value)}


@router.put("/ministries-presentation")
def update_ministries_presentation(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_ministries(parsed)
    setting = upsert_setting(
        session,
        "ministries_presentation_content",
        json.dumps(validated, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/ministries-presentation/reset")
def reset_ministries_presentation(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "ministries_presentation_content",
        json.dumps(DEFAULT_MINISTRIES_PRESENTATION_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_MINISTRIES_PRESENTATION_CONTENT}


@router.post("/ministries-presentation/upload-photo")
async def upload_ministry_leader_photo(
    file: UploadFile = File(...),
    _: str = Depends(get_current_admin),
):
    filename = await save_and_validate_image(file, MINISTRIES_UPLOADS_DIR)
    return {"success": True, "filename": filename, "url": f"/uploads/ministries/{filename}"}


@router.post("/ministries-presentation/upload-media")
async def upload_ministry_media(
    file: UploadFile = File(...),
    _: str = Depends(get_current_admin),
):
    result = await save_and_validate_media(file, MINISTRIES_UPLOADS_DIR)
    filename = result["filename"]
    return {
        "success": True,
        "mediaType": result["mediaType"],
        "filename": filename,
        "url": f"/uploads/ministries/{filename}"
    }


# ─── 6. SERVICES BANNER ──────────────────────────────────────────────────────

@router.get("/services-banner")
def read_services_banner(session: Session = Depends(get_session)):
    setting = get_setting(session, "services_banner_content")
    if not setting:
        setting = upsert_setting(session, "services_banner_content", DEFAULT_SERVICES_BANNER_CONTENT)
    return {"key": "services_banner_content", "value": setting.value}


@router.put("/services-banner")
def update_services_banner(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(session, "services_banner_content", payload.value)
    return {"success": True, "key": setting.key, "value": setting.value}


@router.post("/services-banner/reset")
def reset_services_banner(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(session, "services_banner_content", DEFAULT_SERVICES_BANNER_CONTENT)
    return {"success": True, "key": setting.key, "value": setting.value}


# ─── 7. LOCAL GATHERINGS ────────────────────────────────────────────────────

@router.get("/local-gatherings")
def read_local_gatherings(session: Session = Depends(get_session)):
    setting = get_setting(session, "local_gatherings_content")
    if not setting:
        setting = upsert_setting(
            session,
            "local_gatherings_content",
            json.dumps(DEFAULT_LOCAL_GATHERINGS_CONTENT, ensure_ascii=False)
        )
    parsed = json.loads(setting.value)
    return {"key": "local_gatherings_content", "value": parsed}


@router.put("/local-gatherings")
def update_local_gatherings(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_local_gatherings_content(parsed)
    setting = upsert_setting(session, "local_gatherings_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/local-gatherings/reset")
def reset_local_gatherings(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "local_gatherings_content",
        json.dumps(DEFAULT_LOCAL_GATHERINGS_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_LOCAL_GATHERINGS_CONTENT}


# ─── 8. LOCAL GATHERING OPTIONS ─────────────────────────────────────────────

@router.get("/local-gathering-options")
def read_local_gathering_options(session: Session = Depends(get_session)):
    setting = get_setting(session, "local_gathering_options")
    if not setting:
        setting = upsert_setting(
            session,
            "local_gathering_options",
            json.dumps(DEFAULT_LOCAL_GATHERING_OPTIONS, ensure_ascii=False)
        )
    parsed = json.loads(setting.value)
    return {"key": "local_gathering_options", "value": parsed}


@router.put("/local-gathering-options")
def update_local_gathering_options(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_local_gathering_options(parsed)
    setting = upsert_setting(session, "local_gathering_options", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/local-gathering-options/reset")
def reset_local_gathering_options(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "local_gathering_options",
        json.dumps(DEFAULT_LOCAL_GATHERING_OPTIONS, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_LOCAL_GATHERING_OPTIONS}


# ─── 9. GALLERY ──────────────────────────────────────────────────────────────

@router.get("/gallery")
def read_gallery(session: Session = Depends(get_session)):
    setting = get_setting(session, "gallery_content")
    if not setting:
        setting = upsert_setting(
            session,
            "gallery_content",
            json.dumps(DEFAULT_GALLERY_CONTENT, ensure_ascii=False)
        )
    return {"key": "gallery_content", "value": json.loads(setting.value)}


@router.put("/gallery")
def update_gallery(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_gallery(parsed)
    setting = upsert_setting(session, "gallery_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/gallery/reset")
def reset_gallery(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "gallery_content",
        json.dumps(DEFAULT_GALLERY_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_GALLERY_CONTENT}


@router.post("/gallery/upload-photo")
async def upload_gallery_photo(
    file: UploadFile = File(...),
    _: str = Depends(get_current_admin),
):
    filename = await save_and_validate_image(file, GALLERY_UPLOADS_DIR)
    return {"success": True, "filename": filename, "url": f"/uploads/gallery/{filename}"}


# ─── 10. SOCIAL MEDIA ────────────────────────────────────────────────────────

@router.get("/social-media")
def read_social_media(session: Session = Depends(get_session)):
    setting = get_setting(session, "social_media_content")
    if not setting:
        setting = upsert_setting(
            session,
            "social_media_content",
            json.dumps(DEFAULT_SOCIAL_MEDIA_CONTENT, ensure_ascii=False)
        )
    return {"key": "social_media_content", "value": json.loads(setting.value)}


@router.put("/social-media")
def update_social_media(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_social_media(parsed)
    setting = upsert_setting(session, "social_media_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/social-media/reset")
def reset_social_media(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "social_media_content",
        json.dumps(DEFAULT_SOCIAL_MEDIA_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_SOCIAL_MEDIA_CONTENT}


# ─── 11. DONATIONS ───────────────────────────────────────────────────────────

@router.get("/donations")
def read_donations(session: Session = Depends(get_session)):
    setting = get_setting(session, "donations_content")
    if not setting:
        setting = upsert_setting(
            session,
            "donations_content",
            json.dumps(DEFAULT_DONATIONS_CONTENT, ensure_ascii=False)
        )
    parsed = json.loads(setting.value)
    return {"key": "donations_content", "value": parsed}


@router.put("/donations")
def update_donations(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_donations_content(parsed)
    setting = upsert_setting(session, "donations_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/donations/reset")
def reset_donations(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "donations_content",
        json.dumps(DEFAULT_DONATIONS_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_DONATIONS_CONTENT}


# ─── 12. LOCATIONS ───────────────────────────────────────────────────────────

@router.get("/locations")
def read_locations(session: Session = Depends(get_session)):
    setting = get_setting(session, "locations_content")
    if not setting:
        setting = upsert_setting(
            session,
            "locations_content",
            json.dumps(DEFAULT_LOCATIONS_CONTENT, ensure_ascii=False)
        )
    parsed = json.loads(setting.value)
    return {"key": "locations_content", "value": parsed}


@router.put("/locations")
def update_locations(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_locations(parsed)
    setting = upsert_setting(session, "locations_content", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/locations/reset")
def reset_locations(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "locations_content",
        json.dumps(DEFAULT_LOCATIONS_CONTENT, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_LOCATIONS_CONTENT}


# ─── IFTHENPAY / GATEWAY CONFIG ───────────────────────────────────────────────

@router.get("/ifthenpay-config")
def read_ifthenpay_config(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = get_setting(session, "ifthenpay_config")
    if not setting:
        setting = get_setting(session, "sibs_config")
    if not setting:
        setting = upsert_setting(
            session,
            "ifthenpay_config",
            json.dumps(DEFAULT_IFTHENPAY_CONFIG, ensure_ascii=False)
        )
    parsed = json.loads(setting.value)
    validated = validate_ifthenpay_config(parsed)
    return {"key": "ifthenpay_config", "value": validated}


@router.put("/ifthenpay-config")
def update_ifthenpay_config(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_ifthenpay_config(parsed)
    setting = upsert_setting(session, "ifthenpay_config", json.dumps(validated, ensure_ascii=False))
    # Sincroniza também chave legacy se existir
    upsert_setting(session, "sibs_config", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/ifthenpay-config/reset")
def reset_ifthenpay_config(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "ifthenpay_config",
        json.dumps(DEFAULT_IFTHENPAY_CONFIG, ensure_ascii=False)
    )
    upsert_setting(
        session,
        "sibs_config",
        json.dumps(DEFAULT_IFTHENPAY_CONFIG, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_IFTHENPAY_CONFIG}


# Compatibilidade com endpoints legacy /sibs-config
@router.get("/sibs-config")
def read_sibs_config(
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin)
):
    return read_ifthenpay_config(session=session, _=admin)


@router.put("/sibs-config")
def update_sibs_config(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin)
):
    return update_ifthenpay_config(payload=payload, session=session, _=admin)


@router.post("/sibs-config/reset")
def reset_sibs_config(
    session: Session = Depends(get_session),
    admin: str = Depends(get_current_admin)
):
    return reset_ifthenpay_config(session=session, _=admin)


# ─── GOOGLE MAPS CONFIG ───────────────────────────────────────────────────────

@router.get("/google-maps-config")
def read_google_maps_config(
    session: Session = Depends(get_session),
):
    setting = get_setting(session, "google_maps_config")
    if not setting:
        setting = upsert_setting(
            session,
            "google_maps_config",
            json.dumps(DEFAULT_GOOGLE_MAPS_CONFIG, ensure_ascii=False)
        )
    try:
        parsed = json.loads(setting.value)
    except json.JSONDecodeError:
        parsed = DEFAULT_GOOGLE_MAPS_CONFIG
    validated = validate_google_maps_config(parsed)
    return {"key": "google_maps_config", "value": validated}


@router.put("/google-maps-config")
def update_google_maps_config(
    payload: SettingUpdate,
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    try:
        parsed = json.loads(payload.value)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido")

    validated = validate_google_maps_config(parsed)
    setting = upsert_setting(session, "google_maps_config", json.dumps(validated, ensure_ascii=False))
    return {"success": True, "key": setting.key, "value": validated}


@router.post("/google-maps-config/reset")
def reset_google_maps_config(
    session: Session = Depends(get_session),
    _: str = Depends(get_current_admin)
):
    setting = upsert_setting(
        session,
        "google_maps_config",
        json.dumps(DEFAULT_GOOGLE_MAPS_CONFIG, ensure_ascii=False)
    )
    return {"success": True, "key": setting.key, "value": DEFAULT_GOOGLE_MAPS_CONFIG}

