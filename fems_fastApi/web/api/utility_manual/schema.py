from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class UtilityManualCreateRequest(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    utility_id: str
    utility_name: str | None = None
    source_id: str | None = None
    utility_date: datetime | None = None
    unit: str | None = None
    utility_used: Decimal | None = None
    cre_user: str | None = None


class UtilityManualUpdateRequest(BaseModel):
    plant_code: str | None = None
    utility_name: str | None = None
    source_id: str | None = None             # WHERE 조건 - 기존 SOURCE_ID
    utility_date: datetime | None = None     # WHERE 조건 - 기존 UTILITY_DATE
    af_source_id: str | None = None          # SET 대상 - 변경 후 SOURCE_ID
    af_utility_date: datetime | None = None  # SET 대상 - 변경 후 UTILITY_DATE
    unit: str | None = None
    utility_used: Decimal | None = None
    upd_user: str | None = None


class UtilityManualResponse(BaseModel):
    mill_cd: str | None = None
    plant_code: str | None = None
    utility_id: str | None = None
    utility_name: str | None = None
    source_id: str | None = None
    source_name: str | None = None
    utility_date: datetime | None = None
    unit: str | None = None
    utility_used: Decimal | None = None  # CAST(UTILITY_USED AS DECIMAL(18,2))

    model_config = {"from_attributes": True}
