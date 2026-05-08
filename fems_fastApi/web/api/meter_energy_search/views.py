from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.meter_energy_search.schema import MeterEnergySearchResponse

router = APIRouter()


@router.get("", response_model=list[MeterEnergySearchResponse])
async def get_meter_energy_search(
    session: AsyncSession = Depends(get_db_session),
) -> list[MeterEnergySearchResponse]:
    """실시간 계통별 에너지사용현황 조회 (USP_METER_ENERGY_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_METER_ENERGY_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S'"
    )
    result = await session.execute(sql)
    rows = result.mappings().all()
    return [MeterEnergySearchResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
