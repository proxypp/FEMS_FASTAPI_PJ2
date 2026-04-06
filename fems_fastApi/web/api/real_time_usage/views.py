from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.real_time_usage.schema import RealTimeDayUsageResponse, RealTimeHourUsageResponse, RealTimeMeterResponse, RealTimeMonthUsageResponse, RealTimeUsageResponse

router = APIRouter()


@router.get("", response_model=list[RealTimeUsageResponse])
async def get_real_time_usage(
    session: AsyncSession = Depends(get_db_session),
) -> list[RealTimeUsageResponse]:
    """실시간 사용현황 조회 (USP_REAL_TIME_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S'"
    )
    result = await session.execute(sql)
    rows = result.mappings().all()
    return [RealTimeUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/meter", response_model=list[RealTimeMeterResponse])
async def get_real_time_meter(
    session: AsyncSession = Depends(get_db_session),
) -> list[RealTimeMeterResponse]:
    """실시간 계측기 현황 조회 (USP_REAL_TIME_METER_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_METER_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S'"
    )
    result = await session.execute(sql)
    rows = result.mappings().all()
    return [RealTimeMeterResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/day-usage", response_model=list[RealTimeDayUsageResponse])
async def get_real_time_day_usage(
    rout_code: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[RealTimeDayUsageResponse]:
    """실시간 일별 평균 사용량 조회 (USP_REAL_TIME_DAY_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_DAY_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@ROUT_CODE = :rout_code"
    )
    result = await session.execute(sql, {"rout_code": rout_code})
    rows = result.mappings().all()
    return [RealTimeDayUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/hour-usage", response_model=list[RealTimeHourUsageResponse])
async def get_real_time_hour_usage(
    rout_code: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[RealTimeHourUsageResponse]:
    """실시간 시간별 평균 사용량 조회 (USP_REAL_TIME_HOUR_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_HOUR_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@ROUT_CODE = :rout_code"
    )
    result = await session.execute(sql, {"rout_code": rout_code})
    rows = result.mappings().all()
    return [RealTimeHourUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/month-usage", response_model=list[RealTimeMonthUsageResponse])
async def get_real_time_month_usage(
    rout_code: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[RealTimeMonthUsageResponse]:
    """실시간 월별 사용량 조회 (USP_REAL_TIME_MONTH_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_MONTH_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@ROUT_CODE = :rout_code"
    )
    result = await session.execute(sql, {"rout_code": rout_code})
    rows = result.mappings().all()
    return [RealTimeMonthUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
