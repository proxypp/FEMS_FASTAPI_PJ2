from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_interface.schema import EquipInterfaceResponse

router = APIRouter()


@router.get("", response_model=list[EquipInterfaceResponse])
async def get_equip_interface(
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipInterfaceResponse]:
    """설비 I/F 조회 (USP_EQUIP_INTERFACE - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "DECLARE @RET_MSG VARCHAR(100) = ''; "
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_INTERFACE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@RET_MSG = @RET_MSG OUTPUT"
    )
    result = await session.execute(sql)
    rows = result.mappings().all()
    return [EquipInterfaceResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
