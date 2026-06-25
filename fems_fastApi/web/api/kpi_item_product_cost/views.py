from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.kpi_item_product_cost.schema import COLUMN_MAP, KpiItemProductCostResponse

router = APIRouter()


@router.get("", response_model=list[KpiItemProductCostResponse])
async def get_kpi_item_product_cost(
    item_code: str = Query(default="", description="제품 코드"),
    item_name: str = Query(default="", description="제품명 (부분 검색)"),
    year: str = Query(default="", description="조회 연도 (예: 2026, 미입력 시 당해 연도)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[KpiItemProductCostResponse]:
    """KPI 제품원가(절감률) 조회 (USP_KPI_ITEM_PRODUCT_COST_SEARCH - GRID_GBN='M', DML_GBN='S').

    조회 연도와 직전 연도의 제품별 월간(1~12월) 단위원가와 연평균을 반환한다.
    """
    sql = text(
        "DECLARE @RET_MSG VARCHAR(100) = ''; "
        "SET NOCOUNT ON; "
        "EXEC USP_KPI_ITEM_PRODUCT_COST_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@YEAR = :year, "
        "@ITEM_CODE = :item_code, "
        "@ITEM_NAME = :item_name, "
        "@RET_MSG = @RET_MSG OUTPUT"
    )
    result = await session.execute(
        sql,
        {"year": year, "item_code": item_code, "item_name": item_name},
    )
    # 프로시저는 조건 미충족 또는 CATCH 진입 시 결과셋을 반환하지 않는다.
    # 이 경우 result.mappings()는 ResourceClosedError를 던지므로 먼저 확인한다.
    if not result.returns_rows:
        return []
    rows = result.mappings().all()
    return [
        KpiItemProductCostResponse(
            **{COLUMN_MAP[k]: v for k, v in row.items() if k in COLUMN_MAP}
        )
        for row in rows
    ]
