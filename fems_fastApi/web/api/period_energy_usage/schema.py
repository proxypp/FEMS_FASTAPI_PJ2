from decimal import Decimal

from pydantic import BaseModel, Field


class PeriodEnergyUsageResponse(BaseModel):
    """기간별 에너지 사용량 조회 결과."""

    energy_type: str | None = Field(None, alias="ENERGY_TYPE")
    total_avg: Decimal | None = Field(None, alias="TOTAL_AVG")
    month_01: Decimal | None = Field(None, alias="01월")
    month_02: Decimal | None = Field(None, alias="02월")
    month_03: Decimal | None = Field(None, alias="03월")
    month_04: Decimal | None = Field(None, alias="04월")
    month_05: Decimal | None = Field(None, alias="05월")
    month_06: Decimal | None = Field(None, alias="06월")
    month_07: Decimal | None = Field(None, alias="07월")
    month_08: Decimal | None = Field(None, alias="08월")
    month_09: Decimal | None = Field(None, alias="09월")
    month_10: Decimal | None = Field(None, alias="10월")
    month_11: Decimal | None = Field(None, alias="11월")
    month_12: Decimal | None = Field(None, alias="12월")

    model_config = {"from_attributes": True, "populate_by_name": True}
