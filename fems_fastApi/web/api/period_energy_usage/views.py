from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.period_energy_usage.schema import PeriodEnergyUsageResponse

router = APIRouter()


@router.get("", response_model=list[PeriodEnergyUsageResponse])
async def get_period_energy_usage(
    year: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[PeriodEnergyUsageResponse]:
    """기간별 에너지 사용량 조회 (USP_PERIOD_ENERGY_USAGE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PERIOD_ENERGY_USAGE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@YEAR = :year"
    )
    result = await session.execute(sql, {"year": year})
    rows = result.mappings().all()
    return [PeriodEnergyUsageResponse(**{k: v for k, v in row.items()}) for row in rows]
