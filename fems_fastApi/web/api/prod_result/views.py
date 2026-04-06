from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.prod_result.schema import (
    ProdResultDeleteRequest,
    ProdResultResponse,
    ProdResultSaveRequest,
)

router = APIRouter()


@router.get("", response_model=list[ProdResultResponse])
async def get_prod_results(
    order_no: str = Query(description="작업지시 번호"),
    sub_order: int = Query(description="SUB ORDER"),
    rout_seq: int = Query(description="공정 순서"),
    session: AsyncSession = Depends(get_db_session),
) -> list[ProdResultResponse]:
    """생산실적 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_RESULT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@ORDER_NO = :order_no, "
        "@SUB_ORDER = :sub_order, "
        "@ROUT_SEQ = :rout_seq"
    )
    result = await session.execute(sql, {"order_no": order_no, "sub_order": sub_order, "rout_seq": rout_seq})
    rows = result.mappings().all()
    return [ProdResultResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("")
async def save_prod_result(
    body: ProdResultSaveRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """생산실적 저장 (신규 등록 / 수정)."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_RESULT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'E', "
        "@MILL_CD = :mill_cd, "
        "@ORDER_DT = :start_dt, "
        "@START_DT = :start_dt, "
        "@ORDER_NO = :order_no, "
        "@SUB_ORDER = :sub_order, "
        "@ROUT_SEQ = :rout_seq, "
        "@WORK_SEQ = :work_seq, "
        "@ROUT_CODE = :rout_code, "
        "@EQUIP_CODE = :equip_code, "
        "@ITEM_CODE = :item_code, "
        "@PROD_QTY = :prod_qty, "
        "@BAD_QTY = :bad_qty, "
        "@CRE_USER = :cre_user, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd,
            "start_dt": body.start_dt,
            "order_no": body.order_no,
            "sub_order": body.sub_order,
            "rout_seq": body.rout_seq,
            "work_seq": body.work_seq or 0,
            "rout_code": body.rout_code or "",
            "equip_code": body.equip_code or "",
            "item_code": body.item_code or "",
            "prod_qty": body.prod_qty or 0,
            "bad_qty": body.bad_qty or 0,
            "cre_user": body.cre_user or "",
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"result": "success"}


@router.delete("")
async def delete_prod_result(
    body: ProdResultDeleteRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """생산실적 삭제."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_PROD_RESULT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@ORDER_NO = :order_no, "
        "@SUB_ORDER = :sub_order, "
        "@ROUT_SEQ = :rout_seq, "
        "@WORK_SEQ = :work_seq"
    )
    await session.execute(
        sql,
        {
            "order_no": body.order_no,
            "sub_order": body.sub_order,
            "rout_seq": body.rout_seq,
            "work_seq": body.work_seq,
        },
    )
    await session.commit()
    return {"result": "success"}
