from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.equip_insp_compare.schema import (
    EquipInspCompareResponse,
    EquipInspCompareSummaryResponse,
)

router = APIRouter()


@router.get("", response_model=list[EquipInspCompareResponse])
async def get_equip_insp_compare(
    mill_cd: str = Query(default="", description="MILL_CD"),
    plan_year: str = Query(default="", description="계획 년도 (YYYY)"),
    plan_month: str = Query(default="", description="계획 월 (MM)"),
    equip_code: str = Query(default="", description="설비 코드"),
    equip_name: str = Query(default="", description="설비명"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipInspCompareResponse]:
    """점검계획대비실적 메인 조회 (USP_EQUIP_INSP_COMPARE - GRID_GBN='M', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_INSP_COMPARE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@PLAN_YEAR = :plan_year, "
        "@PLAN_MONTH = :plan_month, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name"
    )
    result = await session.execute(sql, {
        "mill_cd": mill_cd,
        "plan_year": plan_year,
        "plan_month": plan_month,
        "equip_code": equip_code,
        "equip_name": equip_name,
    })
    try:
        rows = result.mappings().all()
    except ResourceClosedError:
        return []
    return [EquipInspCompareResponse(**dict(row)) for row in rows]


@router.get("/summary", response_model=EquipInspCompareSummaryResponse)
async def get_equip_insp_compare_summary(
    mill_cd: str = Query(default="", description="MILL_CD"),
    plan_year: str = Query(default="", description="계획 년도 (YYYY)"),
    plan_month: str = Query(default="", description="계획 월 (MM)"),
    session: AsyncSession = Depends(get_db_session),
) -> EquipInspCompareSummaryResponse:
    """점검계획대비실적 요약 조회 (USP_EQUIP_INSP_COMPARE - GRID_GBN='S', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_INSP_COMPARE "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@MILL_CD = :mill_cd, "
        "@PLAN_YEAR = :plan_year, "
        "@PLAN_MONTH = :plan_month"
    )
    result = await session.execute(sql, {
        "mill_cd": mill_cd,
        "plan_year": plan_year,
        "plan_month": plan_month,
    })
    try:
        row = result.mappings().one_or_none()
    except ResourceClosedError:
        return EquipInspCompareSummaryResponse()
    if row is None:
        return EquipInspCompareSummaryResponse()
    return EquipInspCompareSummaryResponse(**dict(row))
