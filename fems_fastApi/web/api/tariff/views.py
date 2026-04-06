from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.tariff.schema import (
    TariffCreateRequest,
    TariffResponse,
    TariffSourceResponse,
    TariffUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[TariffResponse])
async def get_tariffs(
    tariff_id: str = Query(default="", description="단가 ID (부분 검색)"),
    tariff_name: str = Query(default="", description="단가명 (부분 검색)"),
    use_yn: str = Query(default="", description="사용여부 (Y/N, 미입력 시 전체)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[TariffResponse]:
    """에너지 단가 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_TARIFF "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@TARIFF_ID = :tariff_id, "
        "@TARIFF_NAME = :tariff_name, "
        "@USE_YN = :use_yn"
    )
    result = await session.execute(sql, {"tariff_id": tariff_id, "tariff_name": tariff_name, "use_yn": use_yn})
    rows = result.mappings().all()
    return [TariffResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/{tariff_id}/sources", response_model=list[TariffSourceResponse])
async def get_tariff_sources(
    tariff_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> list[TariffSourceResponse]:
    """단가에 연결된 에너지원 목록 조회."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_TARIFF "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@TARIFF_ID = :tariff_id"
    )
    result = await session.execute(sql, {"tariff_id": tariff_id})
    rows = result.mappings().all()
    return [TariffSourceResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("", status_code=201)
async def create_tariff(
    body: TariffCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """에너지 단가 등록."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_TARIFF "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@TARIFF_ID = :tariff_id, "
        "@SOURCE_ID = :source_id, "
        "@APPLY_DATE = :apply_date, "
        "@TARIFF_NAME = :tariff_name, "
        "@BASE_PRICE = :base_price, "
        "@UNIT_PRICE = :unit_price, "
        "@ETC_PRICE1 = :etc_price1, "
        "@ETC_PRICE2 = :etc_price2, "
        "@ETC_PRICE3 = :etc_price3, "
        "@ETC_PRICE4 = :etc_price4, "
        "@ETC_PRICE5 = :etc_price5, "
        "@TEX_PER = :tex_per, "
        "@ADD_PRICE1 = :add_price1, "
        "@ADD_PRICE2 = :add_price2, "
        "@ADD_PRICE3 = :add_price3, "
        "@ADD_PRICE4 = :add_price4, "
        "@ADD_PRICE5 = :add_price5, "
        "@USE_YN = :use_yn, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "tariff_id": body.tariff_id,
            "source_id": body.source_id or "",
            "apply_date": body.apply_date,
            "tariff_name": body.tariff_name or "",
            "base_price": body.base_price or 0,
            "unit_price": body.unit_price or 0,
            "etc_price1": body.etc_price1 or 0,
            "etc_price2": body.etc_price2 or 0,
            "etc_price3": body.etc_price3 or 0,
            "etc_price4": body.etc_price4 or 0,
            "etc_price5": body.etc_price5 or 0,
            "tex_per": body.tex_per or 0,
            "add_price1": body.add_price1 or 0,
            "add_price2": body.add_price2 or 0,
            "add_price3": body.add_price3 or 0,
            "add_price4": body.add_price4 or 0,
            "add_price5": body.add_price5 or 0,
            "use_yn": body.use_yn,
            "cre_user": body.cre_user or "",
        },
    )
    await session.commit()
    return {"message": "에너지 단가가 등록되었습니다."}


@router.put("/{tariff_id}")
async def update_tariff(
    tariff_id: str,
    body: TariffUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """에너지 단가 수정."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_TARIFF "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@TARIFF_ID = :tariff_id, "
        "@MILL_CD = :mill_cd, "
        "@PLANT_CODE = :plant_code, "
        "@SOURCE_ID = :source_id, "
        "@APPLY_DATE = :apply_date, "
        "@TARIFF_NAME = :tariff_name, "
        "@BASE_PRICE = :base_price, "
        "@UNIT_PRICE = :unit_price, "
        "@ETC_PRICE1 = :etc_price1, "
        "@ETC_PRICE2 = :etc_price2, "
        "@ETC_PRICE3 = :etc_price3, "
        "@ETC_PRICE4 = :etc_price4, "
        "@ETC_PRICE5 = :etc_price5, "
        "@TEX_PER = :tex_per, "
        "@ADD_PRICE1 = :add_price1, "
        "@ADD_PRICE2 = :add_price2, "
        "@ADD_PRICE3 = :add_price3, "
        "@ADD_PRICE4 = :add_price4, "
        "@ADD_PRICE5 = :add_price5, "
        "@USE_YN = :use_yn, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "tariff_id": tariff_id,
            "mill_cd": body.mill_cd or "",
            "plant_code": body.plant_code or "",
            "source_id": body.source_id or "",
            "apply_date": body.apply_date,
            "tariff_name": body.tariff_name or "",
            "base_price": body.base_price or 0,
            "unit_price": body.unit_price or 0,
            "etc_price1": body.etc_price1 or 0,
            "etc_price2": body.etc_price2 or 0,
            "etc_price3": body.etc_price3 or 0,
            "etc_price4": body.etc_price4 or 0,
            "etc_price5": body.etc_price5 or 0,
            "tex_per": body.tex_per or 0,
            "add_price1": body.add_price1 or 0,
            "add_price2": body.add_price2 or 0,
            "add_price3": body.add_price3 or 0,
            "add_price4": body.add_price4 or 0,
            "add_price5": body.add_price5 or 0,
            "use_yn": body.use_yn or "",
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"message": "에너지 단가가 수정되었습니다."}
