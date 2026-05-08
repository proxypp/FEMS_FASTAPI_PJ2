from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator


class EnergySourceCreateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    source_id: str
    source_name: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    use_yn: str = "Y"
    cre_user: str | None = None


class EnergySourceUpdateRequest(BaseModel):
    plant_code: str | None = None
    source_name: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    use_yn: str | None = None
    upd_user: str | None = None


class EnergySourceResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    plant_name: str | None = None
    source_id: str
    source_name: str | None = None
    unit: str | None = None
    energy_type: str | None = None
    energy_type_name: str | None = None
    use_yn: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}


# ── 매출 에너지원단위 조회 (USP_ENERGY_SOURCE_AMOUNT_SEARCH) ─────────────────

class EnergySourceAmountResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    utility_id: str | None = None
    utility_name: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    source_id: str | None = None
    source_name: str | None = None
    utility_date: str | None = None
    unit: str | None = None
    utility_amount: float | None = None

    model_config = {"from_attributes": True}

    @field_validator("utility_date", mode="before")
    @classmethod
    def coerce_date(cls, v: object) -> str | None:
        if v is None:
            return None
        if isinstance(v, (datetime, date)):
            return v.strftime("%Y-%m-%d")
        return str(v)

    @field_validator("utility_amount", mode="before")
    @classmethod
    def coerce_amount(cls, v: object) -> float | None:
        if v is None:
            return None
        if isinstance(v, Decimal):
            return float(v)
        return v
