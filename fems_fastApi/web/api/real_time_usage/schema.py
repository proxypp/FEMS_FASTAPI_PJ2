from decimal import Decimal

from pydantic import BaseModel, Field


class RealTimeUsageResponse(BaseModel):
    """실시간 사용현황 조회 결과."""

    code_name: str | None = None
    kw: Decimal | None = None
    emission: Decimal | None = None

    model_config = {"from_attributes": True}


class RealTimeMeterResponse(BaseModel):
    """실시간 계측기 현황 조회 결과."""

    meter_id: str | None = None
    meter_name: str | None = None
    utility_used: Decimal | None = None

    model_config = {"from_attributes": True}


class RealTimeDayUsageResponse(BaseModel):
    """실시간 일별 평균 사용량 조회 결과."""

    day: str | None = None
    value: Decimal | None = None

    model_config = {"from_attributes": True}


class RealTimeHourUsageResponse(BaseModel):
    """실시간 시간별 평균 사용량 조회 결과."""

    time: str | None = None
    value: Decimal | None = None

    model_config = {"from_attributes": True}


class RealTimeMonthUsageResponse(BaseModel):
    """실시간 월별 사용량 조회 결과."""

    energy_type: str | None = None
    total_avg: Decimal | None = None
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
