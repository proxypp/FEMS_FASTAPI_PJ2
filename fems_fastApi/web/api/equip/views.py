import base64

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, or_, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.equip import Equip
from fems_fastApi.web.api.equip.schema import (
    EquipCreateRequest,
    EquipDailyCheckDeleteRequest,
    EquipDailyCheckResponse,
    EquipDailyCheckSaveRequest,
    EquipDailyCodeDeleteRequest,
    EquipDailyCodeResponse,
    EquipDailyCodeSaveRequest,
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
    result = await session.execute(sql, {
        "equip_code": equip_code,
        "equip_name": equip_name,
    })
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


# ── 설비점검코드 관리 (USP_EQUIP_DAILY_CODE_EDIT) ──────────────────────────

@router.get("/daily-code", response_model=list[EquipDailyCodeResponse])
async def get_equip_daily_code(
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipDailyCodeResponse]:
    """설비점검코드 조회 (USP_EQUIP_DAILY_CODE_EDIT - DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_DAILY_CODE_EDIT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name, "
        "@IMAGE_BIN = NULL"
    )
    result = await session.execute(sql, {"equip_code": equip_code, "equip_name": equip_name})
    rows = result.mappings().all()
    return [EquipDailyCodeResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("/daily-code", status_code=201)
async def save_equip_daily_code(
    body: EquipDailyCodeSaveRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비점검코드 등록/수정 (USP_EQUIP_DAILY_CODE_EDIT - DML_GBN='A')."""
    image_bytes = base64.b64decode(body.image_bin) if body.image_bin else None

    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_DAILY_CODE_EDIT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@ROUT_CODE = :rout_code, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_CHECK = :equip_check, "
        "@MAGM_VAL = :magm_val, "
        "@MAGM_MAX = :magm_max, "
        "@MAGM_MIN = :magm_min, "
        "@STD_MAX = :std_max, "
        "@STD_MIN = :std_min, "
        "@RMAX_VAL = :rmax_val, "
        "@UNIT = :unit, "
        "@REMARK = :remark, "
        "@IMAGE_BIN = :image_bin, "
        "@CRE_USER = :cre_user, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd,
            "rout_code": body.rout_code,
            "equip_code": body.equip_code,
            "equip_check": body.equip_check,
            "magm_val": body.magm_val,
            "magm_max": body.magm_max,
            "magm_min": body.magm_min,
            "std_max": body.std_max,
            "std_min": body.std_min,
            "rmax_val": body.rmax_val,
            "unit": body.unit,
            "remark": body.remark,
            "image_bin": image_bytes,
            "cre_user": body.cre_user,
            "upd_user": body.upd_user,
        },
    )
    await session.commit()
    return {"message": "설비점검코드가 저장되었습니다."}


@router.delete("/daily-code")
async def delete_equip_daily_code(
    body: EquipDailyCodeDeleteRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비점검코드 삭제 (USP_EQUIP_DAILY_CODE_EDIT - DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_DAILY_CODE_EDIT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@MILL_CD = :mill_cd, "
        "@ROUT_CODE = :rout_code, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_CHECK = :equip_check"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd,
            "rout_code": body.rout_code,
            "equip_code": body.equip_code,
            "equip_check": body.equip_check,
        },
    )
    await session.commit()
    return {"message": "설비점검코드가 삭제되었습니다."}


# ── 설비점검실적 관리 (USP_EQUIP_DAILY_CHECK_EDIT) ──────────────────────────

@router.get("/daily-check", response_model=list[EquipDailyCheckResponse])
async def get_equip_daily_check(
    equip_code: str = Query(default="", description="설비 코드 (부분 검색)"),
    equip_name: str = Query(default="", description="설비명 (부분 검색)"),
    check_yyyymm: str = Query(default="", description="점검년월 (YYYYMM)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[EquipDailyCheckResponse]:
    """설비점검실적 조회 (USP_EQUIP_DAILY_CHECK_EDIT - DML_GBN='S')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_DAILY_CHECK_EDIT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'S', "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_NAME = :equip_name, "
        "@CHECK_YYYYMM = :check_yyyymm"
    )
    result = await session.execute(sql, {
        "equip_code": equip_code,
        "equip_name": equip_name,
        "check_yyyymm": check_yyyymm,
    })
    rows = result.mappings().all()
    return [EquipDailyCheckResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("/daily-check", status_code=201)
async def save_equip_daily_check(
    body: EquipDailyCheckSaveRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비점검실적 등록/수정 (USP_EQUIP_DAILY_CHECK_EDIT - DML_GBN='A')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_DAILY_CHECK_EDIT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'A', "
        "@MILL_CD = :mill_cd, "
        "@ROUT_CODE = :rout_code, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_CHECK = :equip_check, "
        "@CHECK_YYYYMM = :check_yyyymm, "
        "@VALUE_1 = :value_1, "
        "@VALUE_2 = :value_2, "
        "@VALUE_3 = :value_3, "
        "@VALUE_4 = :value_4, "
        "@VALUE_5 = :value_5, "
        "@VALUE_6 = :value_6, "
        "@VALUE_7 = :value_7, "
        "@VALUE_8 = :value_8, "
        "@VALUE_9 = :value_9, "
        "@VALUE_10 = :value_10, "
        "@VALUE_11 = :value_11, "
        "@VALUE_12 = :value_12, "
        "@VALUE_13 = :value_13, "
        "@VALUE_14 = :value_14, "
        "@VALUE_15 = :value_15, "
        "@VALUE_16 = :value_16, "
        "@VALUE_17 = :value_17, "
        "@VALUE_18 = :value_18, "
        "@VALUE_19 = :value_19, "
        "@VALUE_20 = :value_20, "
        "@VALUE_21 = :value_21, "
        "@VALUE_22 = :value_22, "
        "@VALUE_23 = :value_23, "
        "@VALUE_24 = :value_24, "
        "@VALUE_25 = :value_25, "
        "@VALUE_26 = :value_26, "
        "@VALUE_27 = :value_27, "
        "@VALUE_28 = :value_28, "
        "@VALUE_29 = :value_29, "
        "@VALUE_30 = :value_30, "
        "@VALUE_31 = :value_31, "
        "@CRE_USER = :cre_user, "
        "@UPD_USER = :upd_user"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd,
            "rout_code": body.rout_code,
            "equip_code": body.equip_code,
            "equip_check": body.equip_check,
            "check_yyyymm": body.check_yyyymm,
            "value_1": body.value_1,
            "value_2": body.value_2,
            "value_3": body.value_3,
            "value_4": body.value_4,
            "value_5": body.value_5,
            "value_6": body.value_6,
            "value_7": body.value_7,
            "value_8": body.value_8,
            "value_9": body.value_9,
            "value_10": body.value_10,
            "value_11": body.value_11,
            "value_12": body.value_12,
            "value_13": body.value_13,
            "value_14": body.value_14,
            "value_15": body.value_15,
            "value_16": body.value_16,
            "value_17": body.value_17,
            "value_18": body.value_18,
            "value_19": body.value_19,
            "value_20": body.value_20,
            "value_21": body.value_21,
            "value_22": body.value_22,
            "value_23": body.value_23,
            "value_24": body.value_24,
            "value_25": body.value_25,
            "value_26": body.value_26,
            "value_27": body.value_27,
            "value_28": body.value_28,
            "value_29": body.value_29,
            "value_30": body.value_30,
            "value_31": body.value_31,
            "cre_user": body.cre_user,
            "upd_user": body.upd_user,
        },
    )
    await session.commit()
    return {"message": "설비점검실적이 저장되었습니다."}


@router.delete("/daily-check")
async def delete_equip_daily_check(
    body: EquipDailyCheckDeleteRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """설비점검실적 삭제 (USP_EQUIP_DAILY_CHECK_EDIT - DML_GBN='D')."""
    sql = text(
        "SET NOCOUNT ON; "
        "EXEC USP_EQUIP_DAILY_CHECK_EDIT "
        "@GRID_GBN = 'M', "
        "@DML_GBN = 'D', "
        "@MILL_CD = :mill_cd, "
        "@ROUT_CODE = :rout_code, "
        "@EQUIP_CODE = :equip_code, "
        "@EQUIP_CHECK = :equip_check, "
        "@CHECK_YYYYMM = :check_yyyymm"
    )
    await session.execute(
        sql,
        {
            "mill_cd": body.mill_cd,
            "rout_code": body.rout_code,
            "equip_code": body.equip_code,
            "equip_check": body.equip_check,
            "check_yyyymm": body.check_yyyymm,
        },
    )
    await session.commit()
    return {"message": "설비점검실적이 삭제되었습니다."}
