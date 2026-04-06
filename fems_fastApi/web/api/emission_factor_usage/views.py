from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.emission_factor_usage.schema import EmissionFactorUsageResponse

router = APIRouter()


@router.get("", response_model=list[EmissionFactorUsageResponse])
async def get_emission_factor_usage(
    utility_id: str = Query(default="", description="유틸리티 ID (부분 검색)"),
    utility_name: str = Query(default="", description="유틸리티 명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EmissionFactorUsageResponse]:
    """배출계수 사용현황 조회 (USP_EMISSION_FACTOR_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EMISSION_FACTOR_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@UTILITY_ID = :utility_id, "
        "@UTILITY_NAME = :utility_name"
    )
    result = await session.execute(
        sql,
        {"utility_id": utility_id, "utility_name": utility_name},
    )
    rows = result.mappings().all()
    return [EmissionFactorUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
