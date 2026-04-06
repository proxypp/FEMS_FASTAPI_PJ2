from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.utility_amount.schema import (
    UtilityAmountCreateRequest,
    UtilityAmountResponse,
    UtilityAmountUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[UtilityAmountResponse])
async def get_utility_amount(
    utility_id: str = Query(default="", description="유틸리티 ID (부분 검색)"),
    utility_name: str = Query(default="", description="유틸리티 명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[UtilityAmountResponse]:
    """유틸리티 비용 목록 조회 (USP_UTILITY_AMOUNT_MANAGEMENT - DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_UTILITY_AMOUNT_MANAGEMENT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@UTILITY_ID = :utility_id, "
        "@UTILITY_NAME = :utility_name"
    )
    result = await session.execute(
        sql,
        {"utility_id": utility_id, "utility_name": utility_name},
    )
    rows = result.mappings().all()
    return [UtilityAmountResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("", status_code=201)
async def create_utility_amount(
    body: UtilityAmountCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """유틸리티 비용 등록 (USP_UTILITY_AMOUNT_MANAGEMENT - DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_UTILITY_AMOUNT_MANAGEMENT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@UTILITY_ID = :utility_id, "
        "@UTILITY_NAME = :utility_name, "
        "@SOURCE_ID = :source_id, "
        "@UTILITY_DATE = :utility_date, "
        "@UNIT = :unit, "
        "@UTILITY_AMOUNT = :utility_amount, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "utility_id": body.utility_id,
            "utility_name": body.utility_name or "",
            "source_id": body.source_id or "",
            "utility_date": body.utility_date,
            "unit": body.unit or "",
            "utility_amount": body.utility_amount or 0,
            "cre_user": body.cre_user or "",
        },
    )
    await session.commit()
    return {"message": "유틸리티 비용이 등록되었습니다."}


@router.put("/{utility_id}")
async def update_utility_amount(
    utility_id: str,
    body: UtilityAmountUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """유틸리티 비용 수정 (USP_UTILITY_AMOUNT_MANAGEMENT - DML_GBN='U').

    - source_id, utility_date : WHERE 조건 (기존값)
    - af_source_id, af_utility_date : SET 대상 (변경 후 값)
    """
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_UTILITY_AMOUNT_MANAGEMENT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@PLANT_CODE = :plant_code, "
        "@UTILITY_ID = :utility_id, "
        "@UTILITY_NAME = :utility_name, "
        "@SOURCE_ID = :source_id, "
        "@AF_SOURCE_ID = :af_source_id, "
        "@UTILITY_DATE = :utility_date, "
        "@AF_UTILITY_DATE = :af_utility_date, "
        "@UNIT = :unit, "
        "@UTILITY_AMOUNT = :utility_amount, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "plant_code": body.plant_code or "",
            "utility_id": utility_id,
            "utility_name": body.utility_name or "",
            "source_id": body.source_id or "",
            "af_source_id": body.af_source_id or body.source_id or "",
            "utility_date": body.utility_date,
            "af_utility_date": body.af_utility_date or body.utility_date,
            "unit": body.unit or "",
            "utility_amount": body.utility_amount or 0,
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"message": "유틸리티 비용이 수정되었습니다."}


@router.delete("/{utility_id}")
async def delete_utility_amount(
    utility_id: str,
    utility_name: str = Query(description="유틸리티 명"),
    source_id: str = Query(description="에너지원 ID"),
    utility_date: str = Query(description="유틸리티 날짜 (YYYY-MM-DD)"),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """유틸리티 비용 삭제 (USP_UTILITY_AMOUNT_MANAGEMENT - DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_UTILITY_AMOUNT_MANAGEMENT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@UTILITY_ID = :utility_id, "
        "@UTILITY_NAME = :utility_name, "
        "@SOURCE_ID = :source_id, "
        "@UTILITY_DATE = :utility_date"
    )
    await session.execute(
        sql,
        {
            "utility_id": utility_id,
            "utility_name": utility_name,
            "source_id": source_id,
            "utility_date": utility_date,
        },
    )
    await session.commit()
    return {"message": "유틸리티 비용이 삭제되었습니다."}
