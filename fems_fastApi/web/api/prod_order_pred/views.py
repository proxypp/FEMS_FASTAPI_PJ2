from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.prod_order_pred.schema import ProdOrderPredResponse

router = APIRouter()


@router.get("", response_model=list[ProdOrderPredResponse])
async def get_prod_order_preds(
    start_dt: str = Query(description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(description="조회 종료일 (YYYY-MM-DD)"),
    rout_code: str = Query(default="", description="공정 코드 (부분 검색)"),
    mill_cd: str = Query(default="1", description="공장 코드"),
    session: AsyncSession = Depends(get_db_session),
) -> list[ProdOrderPredResponse]:
    """작업지시별 사용예측 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_ORDER_PRED_SEARCH "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt, "
        "@ROUT_CODE = :rout_code "
    )
    # @START_DT, @END_DT는 YYYYMMDD(예: 20260617) 형태로 전달한다.
    result = await session.execute(
        sql,
        {
            "mill_cd": mill_cd,
            "start_dt": start_dt.replace("-", ""),
            "end_dt": end_dt.replace("-", ""),
            "rout_code": rout_code,
        },
    )
    rows = result.mappings().all()
    return [ProdOrderPredResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]
