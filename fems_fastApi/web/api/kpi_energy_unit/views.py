from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.kpi_energy_unit.schema import (
    COLUMN_MAP,
    KpiEnergyWonUnitResponse,
)

router = APIRouter()


@router.get("", response_model=list[KpiEnergyWonUnitResponse])
async def get_kpi_energy_unit(
    year: str = Query(default="", description="기준 연도 (예: 2026). 해당 연도와 전년도를 조회"),
    equip_code: str = Query(default="", description="설비 코드"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[KpiEnergyWonUnitResponse]:
    """KPI 에너지 원단위 배출량 조회 (USP_KPI_ENERGY_UNIT_AMOUNT_SEARCH - GRID_GBN='M', DML_GBN='S').

    기준 연도(@YEAR)와 전년도의 설비별 월간(1~12월) 배출원단위와 합계를 반환한다.
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_KPI_ENERGY_UNIT_AMOUNT_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@YEAR = :year, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name "
    )
    result = await session.execute(
        sql,
        {"year": year, "equip_code": equip_code, "equip_name": equip_name},
    )
    # 프로시저는 조건 미충족 또는 CATCH 진입 시 결과셋을 반환하지 않는다.
    # 이 경우 result.mappings()는 ResourceClosedError를 던지므로 먼저 확인한다.
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        KpiEnergyWonUnitResponse(
            **{COLUMN_MAP[k]: v for k, v in row.items() if k in COLUMN_MAP}
        )
        for row in rows
    ]
