from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_result_search.schema import EquipResultSearchResponse

router = APIRouter()


@router.get("", response_model=list[EquipResultSearchResponse])
async def get_equip_result_search(
    mill_cd: str = Query(default="", description="MILL_CD"),
    equip_code: str = Query(default="", description="설비 코드"),
    equip_name: str = Query(default="", description="설비명"),
    start_dt: str = Query(default="", description="시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(default="", description="종료일 (YYYY-MM-DD)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipResultSearchResponse]:
    """설비가동조회 (USP_EQUIP_RESULT_SEARCH - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_RESULT_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name, "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt"
    )
    result = await session.execute(sql, {
        "mill_cd": mill_cd,
        "equip_code": equip_code,
        "equip_name": equip_name,
        "start_dt": start_dt,
        "end_dt": end_dt,
    })
    try:
        rows = result.mappings().all()
    except ResourceClosedError:
        return []
    return [EquipResultSearchResponse(**dict(row)) for row in rows]
