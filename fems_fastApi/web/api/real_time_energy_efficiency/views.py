from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.real_time_energy_efficiency.schema import (
    RealTimeEnergyEfficiencyResponse,
)

router = APIRouter()


@router.get("", response_model=list[RealTimeEnergyEfficiencyResponse])
async def get_real_time_energy_efficiency(
    session: AsyncSession = Depends(get_db_session),
) -> list[RealTimeEnergyEfficiencyResponse]:
    """실시간 에너지 효율 조회 (USP_REAL_TIME_ENERGY_EFFICIENCY_SEARCH - GRID_GBN='M', DML_GBN='S').

    금일/전일 'Kw' 사용량과 전일 대비 금일 사용량 비율(효율, %), 기준일자를 반환한다.
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_REAL_TIME_ENERGY_EFFICIENCY_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S'"
    )
    result = await session.execute(sql)
    # 프로시저는 조건 미충족 또는 CATCH 진입 시 결과셋을 반환하지 않는다.
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        RealTimeEnergyEfficiencyResponse(**{k.lower(): v for k, v in row.items()})
        for row in rows
    ]
