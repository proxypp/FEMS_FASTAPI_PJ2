from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.energy_source.schema import (
    EnergySourceCreateRequest,
    EnergySourceResponse,
    EnergySourceUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[EnergySourceResponse])
async def get_energy_sources(
    source_id: str = Query(default="", description="에너지원 ID (부분 검색)"),
    source_name: str = Query(default="", description="에너지원 명 (부분 검색)"),
    use_yn: str = Query(default="", description="사용여부 (Y: 사용, N: 미사용, 빈값: 전체)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EnergySourceResponse]:
    """에너지원 관리 목록 조회 (SWIT_SP_ENERGY_MANAGEMENT)."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_ENERGY_SOURCE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@SOURCE_ID = :source_id, "
        "@SOURCE_NAME = :source_name, "
        "@USE_YN = :use_yn"
    )
    result = await session.execute(
        sql,
        {"source_id": source_id, "source_name": source_name, "use_yn": use_yn},
    )
    rows = result.mappings().all()

    return [EnergySourceResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("", status_code=201)
async def create_energy_source(
    body: EnergySourceCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """에너지원 등록 (SWIT_SP_ENERGY_MANAGEMENT - DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_ENERGY_SOURCE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@SOURCE_ID = :source_id, "
        "@SOURCE_NAME = :source_name, "
        "@UNIT = :unit, "
        "@ENERGY_TYPE = :energy_type, "
        "@USE_YN = :use_yn, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "source_id": body.source_id,
            "source_name": body.source_name or "",
            "unit": body.unit or "",
            "energy_type": body.energy_type or "",
            "use_yn": body.use_yn,
            "cre_user": body.cre_user or "",
        },
    )
    await session.commit()
    return {"message": "에너지원이 등록되었습니다."}


@router.put("/{source_id}")
async def update_energy_source(
    source_id: str,
    body: EnergySourceUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """에너지원 수정 (SWIT_SP_ENERGY_MANAGEMENT - DML_GBN='U')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_ENERGY_SOURCE "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@SOURCE_ID = :source_id, "
        "@PLANT_CODE = :plant_code, "
        "@SOURCE_NAME = :source_name, "
        "@UNIT = :unit, "
        "@ENERGY_TYPE = :energy_type, "
        "@USE_YN = :use_yn, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "source_id": source_id,
            "plant_code": body.plant_code or "",
            "source_name": body.source_name or "",
            "unit": body.unit or "",
            "energy_type": body.energy_type or "",
            "use_yn": body.use_yn or "",
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"message": "에너지원이 수정되었습니다."}
