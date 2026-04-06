from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.utility_source_usage.schema import (
    UtilitySourceMasterResponse,
    UtilitySourceUsageResponse,
)

router = APIRouter()


@router.get("/master", response_model=list[UtilitySourceMasterResponse])
async def get_utility_source_master(
    source_id: str = Query(default="", description="에너지원 ID (부분 검색)"),
    source_name: str = Query(default="", description="에너지원 명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[UtilitySourceMasterResponse]:
    """에너지원 마스터 목록 조회 (USP_UTILITY_SOURCE_USAGE - GRID_GBN='M')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_UTILITY_SOURCE_USAGE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@SOURCE_ID = :source_id, "
        "@SOURCE_NAME = :source_name"
    )
    result = await session.execute(
        sql,
        {"source_id": source_id, "source_name": source_name},
    )
    rows = result.mappings().all()

    return [UtilitySourceMasterResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/detail", response_model=list[UtilitySourceUsageResponse])
async def get_utility_source_usage(
    source_id: str = Query(..., description="에너지원 ID"),
    session: AsyncSession = Depends(get_db_session),
) -> list[UtilitySourceUsageResponse]:
    """에너지원별 사용현황 상세 조회 (USP_UTILITY_SOURCE_USAGE - GRID_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_UTILITY_SOURCE_USAGE "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@SOURCE_ID = :source_id"
    )
    result = await session.execute(
        sql,
        {"source_id": source_id},
    )
    rows = result.mappings().all()

    return [UtilitySourceUsageResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
