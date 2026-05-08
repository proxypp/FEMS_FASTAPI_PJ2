from decimal import Decimal

from pydantic import BaseModel


class MeterEnergySearchResponse(BaseModel):
    """실시간 계통별 에너지사용현황 조회 결과."""

    equip_code: str | None = None
    vv: Decimal | None = None
    aa: Decimal | None = None
    kw: Decimal | None = None
    kwh: Decimal | None = None

    model_config = {"from_attributes": True}
