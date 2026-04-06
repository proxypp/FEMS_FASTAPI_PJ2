from datetime import datetime

from pydantic import BaseModel


class UtilitySourceMasterResponse(BaseModel):
    """GRID_GBN='M' - 에너지원 마스터 목록."""

    source_id: str
    source_name: str | None = None
    energy_type: str | None = None

    model_config = {"from_attributes": True}


class UtilitySourceUsageResponse(BaseModel):
    """GRID_GBN='S' - 에너지원별 사용현황 상세."""

    source_id: str | None = None
    source_name: str | None = None
    utility_id: str | None = None
    utility_name: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    utility_date: datetime | None = None
    unit: str | None = None
    utility_used: float | None = None

    model_config = {"from_attributes": True}
