from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_alarm.schema import EquipAlarmResponse

router = APIRouter()


@router.get("", response_model=list[EquipAlarmResponse])
async def get_equip_alarms(
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipAlarmResponse]:
    """경보알람 조회 (USP_EQUIP_ALARM - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_ALARM "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name"
    )
    result = await session.execute(sql, {
        "equip_code": equip_code,
        "equip_name": equip_name,
    })
    # 프로시저는 조건 미충족 또는 CATCH 진입 시 결과셋을 반환하지 않는다.
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        EquipAlarmResponse(**{k.lower(): v for k, v in row.items()})
        for row in rows
    ]
