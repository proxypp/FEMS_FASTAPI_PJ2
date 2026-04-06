from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, or_, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.equip import Equip
from fems_fastApi.web.api.equip.schema import (
    EquipCreateRequest,
    EquipMeterCreateRequest,
    EquipMeterResponse,
    EquipMeterUpdateRequest,
    EquipResponse,
    EquipUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[EquipResponse])
async def get_equips(
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    use_yn: str = Query(default="", description="사용여부 (Y: 사용중, N: 폐기, 빈값: 전체)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipResponse]:
    """설비 목록 조회 (EQUIP_CODE/EQUIP_NAME 부분 검색)."""
    query = select(Equip).where(
        Equip.equip_code.like(f"%{equip_code}%"),
        Equip.equip_name.like(f"%{equip_name}%"),
    )

    if use_yn == "Y":
        query = query.where(or_(Equip.disuse_dt == None, Equip.disuse_dt == ""))  # noqa: E711
    elif use_yn == "N":
        query = query.where(and_(Equip.disuse_dt != None, Equip.disuse_dt != ""))  # noqa: E711
    result = await session.execute(query)
    rows = result.scalars().all()

    return [EquipResponse.model_validate(row) for row in rows]


@router.post("", status_code=201)
async def create_equip(
    body: EquipCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비 등록."""
    existing = await session.execute(
        select(Equip).where(Equip.equip_code == body.equip_code),
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="이미 존재하는 설비 코드입니다.")

    equip = Equip(
        mill_cd=body.mill_cd,
        plant_code=body.plant_code,
        equip_code=body.equip_code,
        rout_code=body.rout_code,
        equip_name=body.equip_name,
        equip_gbn=body.equip_gbn,
        equip_type=body.equip_type,
        equip_spec=body.equip_spec,
        buy_dt=body.buy_dt,
        disuse_dt=body.disuse_dt,
        equip_model=body.equip_model,
        equip_cost=body.equip_cost,
        equip_no=body.equip_no,
        equip_tp=body.equip_tp,
        equip_capa=body.equip_capa,
        equip_j=body.equip_j,
        equip_cust=body.equip_cust,
        remark=body.remark,
        cre_user=body.cre_user,
    )
    session.add(equip)
    await session.commit()

    return {"message": "등록되었습니다.", "equip_code": body.equip_code}


@router.put("/{equip_code}")
async def update_equip(
    equip_code: str,
    body: EquipUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비 수정 (EQUIP_CODE 조건, UPD_DT는 현재 시간 자동 설정)."""
    result = await session.execute(
        select(Equip).where(Equip.equip_code == equip_code),
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="설비를 찾을 수 없습니다.")

    values = {k: v for k, v in body.model_dump().items() if v is not None}
    values["upd_dt"] = func.now()

    await session.execute(
        update(Equip).where(Equip.equip_code == equip_code).values(**values),
    )
    await session.commit()

    return {"message": "수정되었습니다.", "equip_code": equip_code}


# ── 설비별 계측기 관리 (USP_BASE_EQUIP_METER) ──────────────────────────────

@router.get("/meter", response_model=list[EquipMeterResponse])
async def get_equip_meter_master(
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipMeterResponse]:
    """설비별 계측기 마스터 조회 - GRID_GBN='M' (설비 코드/설비명 그룹)."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EQUIP_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name"
    )
    result = await session.execute(sql, {"equip_code": equip_code, "equip_name": equip_name})
    rows = result.mappings().all()
    return [EquipMeterResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/{equip_code}/meter/detail", response_model=list[EquipMeterResponse])
async def get_equip_meter_detail(
    equip_code: str,
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipMeterResponse]:
    """설비별 계측기 상세 조회 - GRID_GBN='S' (METER_ID/METER_NAME 포함)."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EQUIP_METER "
        "@GRID_GBN = 'S', "
        "@DML_GBN = 'S', "
        "@EQUIP_CODE = :equip_code"
    )
    result = await session.execute(sql, {"equip_code": equip_code})
    rows = result.mappings().all()
    return [EquipMeterResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("/{equip_code}/meter", status_code=201)
async def create_equip_meter(
    equip_code: str,
    body: EquipMeterCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비별 계측기 등록 (USP_BASE_EQUIP_METER - DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EQUIP_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@EQUIP_CODE = :equip_code, "
        "@METER_ID = :meter_id, "
        "@CRE_USER = :cre_user"
    )
    await session.execute(
        sql,
        {
            "equip_code": equip_code,
            "meter_id": body.meter_id,
            "cre_user": body.cre_user or "",
        },
    )
    await session.commit()
    return {"message": "설비별 계측기가 등록되었습니다."}


@router.put("/{equip_code}/meter/{meter_id}")
async def update_equip_meter(
    equip_code: str,
    meter_id: str,
    body: EquipMeterUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비별 계측기 수정 (USP_BASE_EQUIP_METER - DML_GBN='U')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EQUIP_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'U', "
        "@EQUIP_CODE = :equip_code, "
        "@METER_ID = :meter_id, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "equip_code": equip_code,
            "meter_id": body.meter_id,
            "upd_user": body.upd_user or "",
        },
    )
    await session.commit()
    return {"message": "설비별 계측기가 수정되었습니다."}


@router.delete("/{equip_code}/meter/{meter_id}")
async def delete_equip_meter(
    equip_code: str,
    meter_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비별 계측기 삭제 (USP_BASE_EQUIP_METER - DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_BASE_EQUIP_METER "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@EQUIP_CODE = :equip_code, "
        "@METER_ID = :meter_id"
    )
    await session.execute(sql, {"equip_code": equip_code, "meter_id": meter_id})
    await session.commit()
    return {"message": "설비별 계측기가 삭제되었습니다."}
