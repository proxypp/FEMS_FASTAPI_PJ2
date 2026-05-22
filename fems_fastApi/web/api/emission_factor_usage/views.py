from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.emission_factor_usage.schema import EmissionFactorUsageResponse

router = APIRouter()


@router.get("", response_model=list[EmissionFactorUsageResponse])
async def get_emission_factor_usage(
    mill_cd: str = Query(default="", description="MILL_CD"),
    utility_id: str = Query(default="", description="유틸리티 ID (부분 검색)"),
    utility_name: str = Query(default="", description="유틸리티 명 (부분 검색)"),
    start_dt: str = Query(default="", description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(default="", description="조회 종료일 (YYYY-MM-DD)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EmissionFactorUsageResponse]:
    """배출계수 사용현황 조회 (USP_EMISSION_FACTOR_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EMISSION_FACTOR_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@UTILITY_ID = :utility_id, "
        "@UTILITY_NAME = :utility_name, "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt"
    )
    result = await session.execute(
        sql,
        {
            "mill_cd": mill_cd,
            "utility_id": utility_id,
            "utility_name": utility_name,
            "start_dt": start_dt,
            "end_dt": end_dt,
        },
    )
    rows = result.mappings().all()
    return [EmissionFactorUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
