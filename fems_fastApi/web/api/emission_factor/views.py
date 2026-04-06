from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.emission_factor.schema import (
    EmissionFactorCreateRequest,
    EmissionFactorResponse,
    EmissionFactorSourceResponse,
    EmissionFactorUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[EmissionFactorResponse])
async def get_emission_factors(
    factor_id: str = Query(default="", description="배출계수 ID (부분 검색)"),
    factor_name: str = Query(default="", description="배출계수명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EmissionFactorResponse]:
    """배출계수 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EMISSION_FACTOR "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@FACTOR_ID = :factor_id, "
        "@FACTOR_NAME = :factor_name"
    )
    result = await session.execute(sql, {"factor_id": factor_id, "factor_name": factor_name})
    rows = result.mappings().all()
    return [EmissionFactorResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/{factor_id}/sources", response_model=list[EmissionFactorSourceResponse])
async def get_emission_factor_sources(
    factor_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> list[EmissionFactorSourceResponse]:
    """배출계수에 연결된 에너지원 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EMISSION_FACTOR "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@FACTOR_ID = :factor_id"
    )
    result = await session.execute(sql, {"factor_id": factor_id})
    rows = result.mappings().all()
    return [EmissionFactorSourceResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("", status_code=201)
async def create_emission_factor(
    body: EmissionFactorCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """배출계수 등록."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EMISSION_FACTOR "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@FACTOR_ID = :factor_id, "
        "@SOURCE_ID = :source_id, "
        "@APPLY_DATE = :apply_date, "
        "@FACTOR_NAME = :factor_name, "
        "@FACTOR_VAL = :factor_val, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "factor_id": body.factor_id,
            "source_id": body.source_id or "",
            "apply_date": body.apply_date,
            "factor_name": body.factor_name or "",
            "factor_val": body.factor_val or 0,
            "cre_user": body.cre_user or "",
        },
    )
    await session.commit()
    return {"message": "배출계수가 등록되었습니다."}


@router.put("/{factor_id}")
async def update_emission_factor(
    factor_id: str,
    body: EmissionFactorUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """배출계수 수정."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EMISSION_FACTOR "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@FACTOR_ID = :factor_id, "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@SOURCE_ID = :source_id, "
        "@APPLY_DATE = :apply_date, "
        "@FACTOR_NAME = :factor_name, "
        "@FACTOR_VAL = :factor_val, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "factor_id": factor_id,
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "source_id": body.source_id or "",
            "apply_date": body.apply_date,
            "factor_name": body.factor_name or "",
            "factor_val": body.factor_val or 0,
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"message": "배출계수가 수정되었습니다."}
