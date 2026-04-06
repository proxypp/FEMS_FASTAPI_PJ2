from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.prod_order.schema import ProdOrderDeleteRequest, ProdOrderResponse, ProdOrderSaveRequest

router = APIRouter()


@router.get("", response_model=list[ProdOrderResponse])
async def get_prod_orders(
    start_dt: str = Query(description="조회 시작일 (YYYY-MM-DD)"),
    end_dt: str = Query(description="조회 종료일 (YYYY-MM-DD)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[ProdOrderResponse]:
    """생산작업 지시 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_ORDER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@START_DT = :start_dt, "
        "@END_DT = :end_dt"
    )
    result = await session.execute(sql, {"start_dt": start_dt, "end_dt": end_dt})
    rows = result.mappings().all()
    return [ProdOrderResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("")
async def save_prod_order(
    body: ProdOrderSaveRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """생산작업 지시 저장 (신규 등록 / 수정)."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_ORDER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'E', "
        "@MILL_CD = :mill_cd, "
        "@ORDER_DT = :order_dt, "
        "@ORDER_NO = :order_no, "
        "@SUB_ORDER = :sub_order, "
        "@ROUT_SEQ = :rout_seq, "
        "@ROUT_CODE = :rout_code, "
        "@EQUIP_CODE = :equip_code, "
        "@ITEM_CODE = :item_code, "
        "@ORDER_QTY = :order_qty, "
        "@CRE_USER = :cre_user, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd,
            "order_dt": body.order_dt,
            "order_no": body.order_no or "",
            "sub_order": body.sub_order or 0,
            "rout_seq": body.rout_seq or 0,
            "rout_code": body.rout_code or "",
            "equip_code": body.equip_code or "",
            "item_code": body.item_code or "",
            "order_qty": body.order_qty or 0,
            "cre_user": body.cre_user or "",
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"result": "success"}


@router.delete("")
async def delete_prod_order(
    body: ProdOrderDeleteRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """생산작업 지시 삭제."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_ORDER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@ORDER_NO = :order_no, "
        "@SUB_ORDER = :sub_order, "
        "@ROUT_SEQ = :rout_seq"
    )
    await session.execute(
        sql,
        {
            "order_no": body.order_no,
            "sub_order": body.sub_order,
            "rout_seq": body.rout_seq,
        },
    )
    await session.commit()
    return {"result": "success"}
