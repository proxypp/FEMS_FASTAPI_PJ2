from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.kpi_prod_hour.schema import COLUMN_MAP, KpiProdHourResponse

router = APIRouter()


@router.get("", response_model=list[KpiProdHourResponse])
async def get_kpi_prod_hour(
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    year: str = Query(default="", description="조회 연도 (예: 2026)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[KpiProdHourResponse]:
    """KPI 시간당 생산량 그래프 조회 (USP_KPI_PROD_HOUR - GRID_GBN='M', DML_GBN='S').

    연도별 월간(1~12월) 시간당 생산량과 합계를 반환한다.
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_KPI_PROD_HOUR "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name, "
        "@YEAR = :year "
    )
    result = await session.execute(
        sql,
        {"equip_code": equip_code, "equip_name": equip_name, "year": year},
    )
    # 프로시저는 EXISTS/조건 미충족 또는 CATCH 진입 시 결과셋을 반환하지 않는다.
    # 이 경우 result.mappings()는 ResourceClosedError를 던지므로 먼저 확인한다.
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        KpiProdHourResponse(
            **{COLUMN_MAP[k]: v for k, v in row.items() if k in COLUMN_MAP}
        )
        for row in rows
    ]
