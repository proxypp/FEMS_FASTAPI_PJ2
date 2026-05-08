from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_compare.schema import EquipCompareResponse

router = APIRouter()


@router.get("", response_model=list[EquipCompareResponse])
async def get_equip_compare(
    start_dt: str = Query(default="", description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(default="", description="조회 종료일 (YYYY-MM-DD)"),
    rout_code: str = Query(default="", description="공정 코드"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipCompareResponse]:
    """설비간 비교분석 조회 (USP_EQUIP_COMPARE_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_COMPARE_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt, "
        "@ROUT_CODE = :rout_code"
    )
    result = await session.execute(sql, {
        "start_dt": start_dt,
        "end_dt": end_dt,
        "rout_code": rout_code,
    })
    rows = result.mappings().all()
    return [EquipCompareResponse(**{k: v for k, v in row.items()}) for row in rows]
