from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PeakTrendResponse(BaseModel):
    """오늘 15분 추이 (GRID_GBN='P', DML_GBN='S').

    금일 15분 단위 시간대별 수요전력(Demand)과 당일 피크 시간대 여부(IsPeak)를 반환한다.
    """

    time: str | None = None  # 시간대 (HH:mm)
    slot_dt: datetime | None = Field(default=None, alias="slotdt")  # 슬롯 시각
    demand: Decimal | None = None  # 수요전력 (kW)
    # 프로시저의 IsPeak 컬럼은 소문자화하면 ispeak가 되므로 alias로 매핑한다.
    is_peak: int | None = Field(default=None, alias="ispeak")  # 피크 시간대 여부 (1: 피크, 0: 일반)

    model_config = {"from_attributes": True, "populate_by_name": True}


class PeakMonthlyResponse(BaseModel):
    """월간 일별 최대 (GRID_GBN='P', DML_GBN='M').

    해당 월의 일자별 최대 수요전력(PeakKw)을 반환한다.
    """

    day: int | None = None  # 일자
    peak_kw: Decimal | None = Field(default=None, alias="peakkw")  # 일별 최대 수요전력 (kW)

    model_config = {"from_attributes": True, "populate_by_name": True}


class PeakKpiResponse(BaseModel):
    """피크 KPI (GRID_GBN='P', DML_GBN='K').

    오늘/월간 피크 수요전력과 발생시각, 계약전력을 반환한다.
    """

    today_peak_kw: Decimal | None = Field(default=None, alias="todaypeakkw")  # 금일 피크 (kW)
    today_peak_time: datetime | None = Field(default=None, alias="todaypeaktime")  # 금일 피크 발생시각
    month_peak_kw: Decimal | None = Field(default=None, alias="monthpeakkw")  # 월간 피크 (kW)
    month_peak_time: datetime | None = Field(default=None, alias="monthpeaktime")  # 월간 피크 발생시각
    contract_kw: Decimal | None = Field(default=None, alias="contractkw")  # 계약전력 (kW)

    model_config = {"from_attributes": True, "populate_by_name": True}
