from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.month_prod_emission.schema import MonthProdEmissionResponse

router = APIRouter()


@router.get("/production", response_model=list[MonthProdEmissionResponse])
async def get_month_production(
    year: str = Query(..., description="조회 연도 (YYYY, 예: 2026)"),
    mill_cd: str = Query(default="", description="공장 코드"),
    session: AsyncSession = Depends(get_db_session),
) -> list[MonthProdEmissionResponse]:
    """월 생산량 조회 (USP_MONTH_PROD_EMISSION_SEARCH - GRID_GBN='M')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_MONTH_PROD_EMISSION_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@YEAR = :year"
    )
    result = await session.execute(sql, {"mill_cd": mill_cd, "year": year})
    rows = result.mappings().all()
    return [MonthProdEmissionResponse.model_validate(dict(row)) for row in rows]


@router.get("/emission", response_model=list[MonthProdEmissionResponse])
async def get_month_emission(
    year: str = Query(..., description="조회 연도 (YYYY, 예: 2026)"),
    mill_cd: str = Query(default="", description="공장 코드"),
    session: AsyncSession = Depends(get_db_session),
) -> list[MonthProdEmissionResponse]:
    """월 배출량 조회 (USP_MONTH_PROD_EMISSION_SEARCH - GRID_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_MONTH_PROD_EMISSION_SEARCH "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@YEAR = :year"
    )
    result = await session.execute(sql, {"mill_cd": mill_cd, "year": year})
    rows = result.mappings().all()
    return [MonthProdEmissionResponse.model_validate(dict(row)) for row in rows]
