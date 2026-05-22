from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.energy_usage_pred.schema import EnergyUsagePredResponse

router = APIRouter()


@router.get("", response_model=list[EnergyUsagePredResponse])
async def get_energy_usage_pred(
    start_dt: str = Query(default="", description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(default="", description="조회 종료일 (YYYY-MM-DD)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EnergyUsagePredResponse]:
    """에너지 사용예측 조회 (USP_ENERGY_USAGE_PRED_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_ENERGY_USAGE_PRED_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt"
    )
    result = await session.execute(sql, {
        "start_dt": start_dt,
        "end_dt": end_dt,
    })
    try:
        rows = result.mappings().all()
    except ResourceClosedError:
        return []
    return [EnergyUsagePredResponse(**dict(row)) for row in rows]
