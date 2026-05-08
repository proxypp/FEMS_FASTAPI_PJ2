from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_plan_yymm.schema import (
    EquipPlanYymmDeleteRequest,
    EquipPlanYymmResponse,
    EquipPlanYymmSaveRequest,
)

router = APIRouter()


@router.get("", response_model=list[EquipPlanYymmResponse])
async def get_equip_plan_yymm(
    mill_cd: str = Query(default="", description="MILL_CD"),
    plan_year: str = Query(default="", description="계획 년도 (YYYY)"),
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipPlanYymmResponse]:
    """년월간 설비점검계획 조회 (USP_EQUIP_PLAN_YYMM - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_PLAN_YYMM "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@PLAN_YEAR = :plan_year, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name"
    )
    result = await session.execute(sql, {
        "mill_cd": mill_cd,
        "plan_year": plan_year,
        "equip_code": equip_code,
        "equip_name": equip_name,
    })
    rows = result.mappings().all()
    return [EquipPlanYymmResponse(**dict(row)) for row in rows]


@router.post("", status_code=201)
async def save_equip_plan_yymm(
    body: EquipPlanYymmSaveRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """년월간 설비점검계획 등록/수정 (USP_EQUIP_PLAN_YYMM - GRID_GBN='M', DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_PLAN_YYMM "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@PLAN_YEAR = :plan_year, "
        "@EQUIP_CODE = :equip_code, "
        "@PLAN_DATE01 = :plan_date01, "
        "@PLAN_DATE02 = :plan_date02, "
        "@PLAN_DATE03 = :plan_date03, "
        "@PLAN_DATE04 = :plan_date04, "
        "@PLAN_DATE05 = :plan_date05, "
        "@PLAN_DATE06 = :plan_date06, "
        "@PLAN_DATE07 = :plan_date07, "
        "@PLAN_DATE08 = :plan_date08, "
        "@PLAN_DATE09 = :plan_date09, "
        "@PLAN_DATE10 = :plan_date10, "
        "@PLAN_DATE11 = :plan_date11, "
        "@PLAN_DATE12 = :plan_date12, "
        "@CRE_USER = :cre_user, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(sql, {
        "mill_cd": body.mill_cd,
        "plan_year": body.plan_year,
        "equip_code": body.equip_code,
        "plan_date01": body.plan_date01,
        "plan_date02": body.plan_date02,
        "plan_date03": body.plan_date03,
        "plan_date04": body.plan_date04,
        "plan_date05": body.plan_date05,
        "plan_date06": body.plan_date06,
        "plan_date07": body.plan_date07,
        "plan_date08": body.plan_date08,
        "plan_date09": body.plan_date09,
        "plan_date10": body.plan_date10,
        "plan_date11": body.plan_date11,
        "plan_date12": body.plan_date12,
        "cre_user": body.cre_user,
        "upd_user": body.upd_user,
    })
    await session.commit()
    return {"message": "년월간 설비점검계획이 저장되었습니다."}


@router.delete("")
async def delete_equip_plan_yymm(
    body: EquipPlanYymmDeleteRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """년월간 설비점검계획 삭제 (USP_EQUIP_PLAN_YYMM - GRID_GBN='M', DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_PLAN_YYMM "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@MILL_CD = :mill_cd, "
        "@EQUIP_CODE = :equip_code, "
        "@PLAN_YEAR = :plan_year"
    )
    await session.execute(sql, {
        "mill_cd": body.mill_cd,
        "equip_code": body.equip_code,
        "plan_year": body.plan_year,
    })
    await session.commit()
    return {"message": "년월간 설비점검계획이 삭제되었습니다."}
