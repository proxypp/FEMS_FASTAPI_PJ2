from decimal import Decimal

from pydantic import BaseModel, Field


class PrevYearMonthCompareCurrentResponse(BaseModel):
    """전년/전월 비교분석 - 당해연도 (GRID_GBN='M')."""

    energy_type: str | None = Field(None, alias="ENERGY_TYPE")
    unit: str | None = Field(None, alias="UNIT")
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


class PrevYearMonthComparePreviousResponse(BaseModel):
    """전년/전월 비교분석 - 전년도 (GRID_GBN='S')."""

    energy_type: str | None = Field(None, alias="ENERGY_TYPE")
    unit: str | None = Field(None, alias="UNIT")
    total_avg: Decimal | None = Field(None, alias="TOTAL_AVG")
    month_01: Decimal | None = Field(None, alias="M01")
    month_02: Decimal | None = Field(None, alias="M02")
    month_03: Decimal | None = Field(None, alias="M03")
    month_04: Decimal | None = Field(None, alias="M04")
    month_05: Decimal | None = Field(None, alias="M05")
    month_06: Decimal | None = Field(None, alias="M06")
    month_07: Decimal | None = Field(None, alias="M07")
    month_08: Decimal | None = Field(None, alias="M08")
    month_09: Decimal | None = Field(None, alias="M09")
    month_10: Decimal | None = Field(None, alias="M10")
    month_11: Decimal | None = Field(None, alias="M11")
    month_12: Decimal | None = Field(None, alias="M12")

    model_config = {"from_attributes": True, "populate_by_name": True}
