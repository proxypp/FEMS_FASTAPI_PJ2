from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.mes_interface.schema import MesInterfaceResponse

router = APIRouter()


@router.get("", response_model=list[MesInterfaceResponse])
async def get_mes_interface(
    start_dt: str = Query(description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(description="조회 종료일 (YYYY-MM-DD)"),
    rout_code: str = Query(default="", description="공정 코드 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[MesInterfaceResponse]:
    """MES I/F 조회 (USP_MES_INTERFACE - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "DECLARE @RET_MSG VARCHAR(100) = ''; "
        "SET NOCOUNT ON; "
        "EXEC USP_MES_INTERFACE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt, "
        "@ROUT_CODE = :rout_code, "
        "@RET_MSG = @RET_MSG OUTPUT"
    )
    # @START_DT, @END_DT는 YYYYMMDD(예: 20260617) 형태로 전달한다.
    result = await session.execute(
        sql,
        {
            "start_dt": start_dt.replace("-", ""),
            "end_dt": end_dt.replace("-", ""),
            "rout_code": rout_code,
        },
    )
    rows = result.mappings().all()
    return [MesInterfaceResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
