from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.real_time_peak_15min.schema import (
    PeakKpiResponse,
    PeakMonthlyResponse,
    PeakTrendResponse,
)

router = APIRouter()


@router.get("/trend", response_model=list[PeakTrendResponse])
async def get_peak_trend(
    session: AsyncSession = Depends(get_db_session),
) -> list[PeakTrendResponse]:
    """오늘 15분 추이 (USP_REAL_TIME_PEAK_15MIN_SEARCH - GRID_GBN='P', DML_GBN='S').

    금일 15분 단위 시간대별 수요전력(Demand, kW)과 당일 피크 시간대 여부(IsPeak)를 반환한다.
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_PEAK_15MIN_SEARCH "
        "@GRID_GBN = 'P', "
        "@DML_GBN = 'S'"
    )
    result = await session.execute(sql)
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        PeakTrendResponse(**{k.lower(): v for k, v in row.items()}) for row in rows
    ]


@router.get("/monthly", response_model=list[PeakMonthlyResponse])
async def get_peak_monthly(
    yyyymm: str = Query("", description="조회 월 (YYYYMM). 미지정 시 이번 달"),
    session: AsyncSession = Depends(get_db_session),
) -> list[PeakMonthlyResponse]:
    """월간 일별 최대 (USP_REAL_TIME_PEAK_15MIN_SEARCH - GRID_GBN='P', DML_GBN='M').

    해당 월의 일자별 최대 수요전력(PeakKw)을 반환한다.
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_PEAK_15MIN_SEARCH "
        "@GRID_GBN = 'P', "
        "@DML_GBN = 'M', "
        "@YYYYMM = :yyyymm"
    )
    result = await session.execute(sql, {"yyyymm": yyyymm})
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        PeakMonthlyResponse(**{k.lower(): v for k, v in row.items()}) for row in rows
    ]


@router.get("/kpi", response_model=PeakKpiResponse | None)
async def get_peak_kpi(
    yyyymm: str = Query("", description="조회 월 (YYYYMM). 미지정 시 이번 달"),
    session: AsyncSession = Depends(get_db_session),
) -> PeakKpiResponse | None:
    """피크 KPI (USP_REAL_TIME_PEAK_15MIN_SEARCH - GRID_GBN='P', DML_GBN='K').

    오늘/월간 피크 수요전력과 발생시각, 계약전력을 반환한다.
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_PEAK_15MIN_SEARCH "
        "@GRID_GBN = 'P', "
        "@DML_GBN = 'K', "
        "@YYYYMM = :yyyymm"
    )
    result = await session.execute(sql, {"yyyymm": yyyymm})
    if not result.returns_rows:
        return None
    row = result.mappings().first()
    if row is None:
        return None
    return PeakKpiResponse(**{k.lower(): v for k, v in row.items()})
