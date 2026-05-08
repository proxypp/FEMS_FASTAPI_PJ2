from datetime import datetime

from pydantic import BaseModel


class ItemCreateRequest(BaseModel):
    """Item create request schema."""

    mill_cd: str | None = None
    item_code: str
    item_name: str | None = None
    item_type: str | None = None
    item_wet: float | None = None
    start_dt: str | None = None
    end_dt: str | None = None
    grade: str | None = None
    color: str | None = None
    remark: str | None = None
    cre_user: str


class ItemUpdateRequest(BaseModel):
    """Item update request schema."""

    item_name: str | None = None
    item_type: str | None = None
    item_wet: float | None = None
    start_dt: str | None = None
    end_dt: str | None = None
    grade: str | None = None
    color: str | None = None
    remark: str | None = None
    upd_user: str | None = None


class ItemResponse(BaseModel):
    """Item response schema."""

    mill_cd: str | None = None
    item_code: str
    item_name: str | None = None
    item_type: str | None = None
    item_wet: float | None = None
    start_dt: str | None = None
    end_dt: str | None = None
    grade: str | None = None
    color: str | None = None
    remark: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}


# ── 제품별 원단위 조회 (USP_ITEM_SOURCE_SEARCH) ──────────────────────────────

class ItemSourceResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    item_code: str | None = None
    item_name: str | None = None
    source_id: str | None = None
    source_name: str | None = None
    unit: str | None = None
    unit_used: float | None = None

    model_config = {"from_attributes": True}
