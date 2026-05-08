from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_plan_mmdd.schema import (
    EquipPlanMmddDeleteRequest,
    EquipPlanMmddResponse,
    EquipPlanMmddSaveRequest,
)

router = APIRouter()


@router.get("", response_model=list[EquipPlanMmddResponse])
async def get_equip_plan_mmdd(
    yyyy: str = Query(default="", description="계획 년도 (YYYY)"),
    mm: str = Query(default="", description="계획 월 (MM)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipPlanMmddResponse]:
    """월일간 설비점검계획 조회 (USP_EQUIP_PLAN_MMDD - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_PLAN_MMDD "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@YYYY = :yyyy, "
        "@MM = :mm"
    )
    result = await session.execute(sql, {
        "yyyy": yyyy,
        "mm": mm,
    })
    rows = result.mappings().all()
    return [EquipPlanMmddResponse(**dict(row)) for row in rows]


@router.post("", status_code=201)
async def save_equip_plan_mmdd(
    body: EquipPlanMmddSaveRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """월일간 설비점검계획 등록/수정 (USP_EQUIP_PLAN_MMDD - GRID_GBN='M', DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_PLAN_MMDD "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@YYYY = :yyyy, "
        "@MM = :mm, "
        "@DD = :dd, "
        "@EQUIP_CODE = :equip_code, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(sql, {
        "mill_cd": body.mill_cd,
        "yyyy": body.yyyy,
        "mm": body.mm,
        "dd": body.dd,
        "equip_code": body.equip_code,
        "cre_user": body.cre_user,
    })
    await session.commit()
    return {"message": "월일간 설비점검계획이 저장되었습니다."}


@router.delete("")
async def delete_equip_plan_mmdd(
    body: EquipPlanMmddDeleteRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """월일간 설비점검계획 삭제 (USP_EQUIP_PLAN_MMDD - GRID_GBN='M', DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_PLAN_MMDD "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@MILL_CD = :mill_cd, "
        "@YYYY = :yyyy, "
        "@MM = :mm, "
        "@EQUIP_CODE = :equip_code"
    )
    await session.execute(sql, {
        "mill_cd": body.mill_cd,
        "yyyy": body.yyyy,
        "mm": body.mm,
        "equip_code": body.equip_code,
    })
    await session.commit()
    return {"message": "월일간 설비점검계획이 삭제되었습니다."}
