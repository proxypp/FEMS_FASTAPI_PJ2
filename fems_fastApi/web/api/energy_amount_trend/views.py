from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.energy_amount_trend.schema import EnergyAmountTrendResponse

router = APIRouter()


@router.get("", response_model=list[EnergyAmountTrendResponse])
async def get_energy_amount_trend(
    start_dt: str = Query(default="", description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(default="", description="조회 종료일 (YYYY-MM-DD)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EnergyAmountTrendResponse]:
    """에너지 단가 추이 조회 (USP_ENERGY_AMOUNT_TREND_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_ENERGY_AMOUNT_TREND_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt"
    )
    result = await session.execute(sql, {
        "start_dt": start_dt,
        "end_dt": end_dt,
    })
    rows = result.mappings().all()
    return [EnergyAmountTrendResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
