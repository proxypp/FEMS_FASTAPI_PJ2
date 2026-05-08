from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.prev_year_month_compare.schema import (
    PrevYearMonthCompareCurrentResponse,
    PrevYearMonthComparePreviousResponse,
)

router = APIRouter()


@router.get("/current", response_model=list[PrevYearMonthCompareCurrentResponse])
async def get_prev_year_month_compare_current(
    year: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[PrevYearMonthCompareCurrentResponse]:
    """전년/전월 비교분석 - 당해연도 조회 (GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC [USP_PREVIOUS_YEAR/MONTH_COMPARE_SEARCH] "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@YEAR = :year"
    )
    result = await session.execute(sql, {"year": year})
    rows = result.mappings().all()
    return [PrevYearMonthCompareCurrentResponse(**{k: v for k, v in row.items()}) for row in rows]


@router.get("/previous", response_model=list[PrevYearMonthComparePreviousResponse])
async def get_prev_year_month_compare_previous(
    year: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[PrevYearMonthComparePreviousResponse]:
    """전년/전월 비교분석 - 전년도 조회 (GRID_GBN='S', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC [USP_PREVIOUS_YEAR/MONTH_COMPARE_SEARCH] "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@YEAR = :year"
    )
    result = await session.execute(sql, {"year": year})
    rows = result.mappings().all()
    return [PrevYearMonthComparePreviousResponse(**{k: v for k, v in row.items()}) for row in rows]
