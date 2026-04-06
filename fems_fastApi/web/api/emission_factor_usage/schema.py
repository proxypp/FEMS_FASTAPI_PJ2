from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class EmissionFactorUsageResponse(BaseModel):
    """배출계수 사용현황 조회 결과."""

    source_id: str | None = None
    source_name: str | None = None
    energy_type: str | None = None
    utility_id: str | None = None
    utility_name: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    utility_date: datetime | None = None
    unit: str | None = None
    utility_used: Decimal | None = None
    factor_val: Decimal | None = None
    emission: Decimal | None = None

    model_config = {"from_attributes": True}
