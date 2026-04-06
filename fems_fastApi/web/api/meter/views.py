from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.meter.schema import (
    MeterCreateRequest,
    MeterResponse,
    MeterSourceResponse,
    MeterUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[MeterResponse])
async def get_meters(
    meter_id: str = Query(default="", description="계측기 ID (부분 검색)"),
    meter_name: str = Query(default="", description="계측기 명 (부분 검색)"),
    use_yn: str = Query(default="", description="사용여부 (Y: 사용, N: 미사용, 빈값: 전체)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[MeterResponse]:
    """계측기 목록 조회 (USP_BASE_METER - DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@METER_ID = :meter_id, "
        "@METER_NAME = :meter_name, "
        "@USE_YN = :use_yn"
    )
    result = await session.execute(
        sql,
        {"meter_id": meter_id, "meter_name": meter_name, "use_yn": use_yn},
    )
    rows = result.mappings().all()

    return [MeterResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("", status_code=201)
async def create_meter(
    body: MeterCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """계측기 등록 (USP_BASE_METER - DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@METER_ID = :meter_id, "
        "@METER_NAME = :meter_name, "
        "@METER_TYPE = :meter_type, "
        "@METER_IP = :meter_ip, "
        "@ADDRESS = :address, "
        "@SOURCE_ID = :source_id, "
        "@USE_YN = :use_yn, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "meter_id": body.meter_id,
            "meter_name": body.meter_name or "",
            "meter_type": body.meter_type or "",
            "meter_ip": body.meter_ip or "",
            "address": body.address or "",
            "source_id": body.source_id or "",
            "use_yn": body.use_yn,
            "cre_user": body.cre_user or "",
        },
    )
    await session.commit()
    return {"message": "계측기가 등록되었습니다."}


@router.get("/{meter_id}/source", response_model=list[MeterSourceResponse])
async def get_meter_sources(
    meter_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> list[MeterSourceResponse]:
    """계측기별 에너지원 조회 (USP_BASE_METER - GRID_GBN='S', DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_METER "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@METER_ID = :meter_id"
    )
    result = await session.execute(sql, {"meter_id": meter_id})
    rows = result.mappings().all()

    return [MeterSourceResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.put("/{meter_id}")
async def update_meter(
    meter_id: str,
    body: MeterUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """계측기 수정 (USP_BASE_METER - DML_GBN='U')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@METER_ID = :meter_id, "
        "@PLANT_CODE = :plant_code, "
        "@METER_NAME = :meter_name, "
        "@METER_TYPE = :meter_type, "
        "@METER_IP = :meter_ip, "
        "@ADDRESS = :address, "
        "@SOURCE_ID = :source_id, "
        "@USE_YN = :use_yn, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "meter_id": meter_id,
            "plant_code": body.plant_code or "",
            "meter_name": body.meter_name or "",
            "meter_type": body.meter_type or "",
            "meter_ip": body.meter_ip or "",
            "address": body.address or "",
            "source_id": body.source_id or "",
            "use_yn": body.use_yn or "",
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"message": "계측기가 수정되었습니다."}
