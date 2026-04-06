from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.base_code import BaseCode
from fems_fastApi.web.api.base_code.schema import BaseCodeCreateRequest, BaseCodeResponse, BaseCodeUpdateRequest, RefCodeResponse, SubCodeResponse

router = APIRouter()


@router.get("", response_model=list[BaseCodeResponse])
async def get_base_codes(
    main_code: str | None = Query(None, description="MAIN_CODE 검색어 (부분 일치)"),
    code_name: str | None = Query(None, description="CODE_NAME 검색어 (부분 일치)"),
    use_yn: str | None = Query(None, description="USE_YN 검색어 (부분 일치)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[BaseCodeResponse]:
    """메인 코드 목록 조회 (CODE_LVL = '1')."""
    query = select(BaseCode.main_code, BaseCode.code_name).where(BaseCode.code_lvl == "1").where(BaseCode.sub_code == "$")

    if main_code:
        query = query.where(BaseCode.main_code.like(f"%{main_code}%"))
    if code_name:
        query = query.where(BaseCode.code_name.like(f"%{code_name}%"))
    if use_yn:
        query = query.where(BaseCode.use_yn.like(f"%{use_yn}%"))

    result = await session.execute(query)
    rows = result.all()

    return [BaseCodeResponse(main_code=row.main_code, code_name=row.code_name) for row in rows]


@router.get("/ref", response_model=list[RefCodeResponse])
async def get_codes_by_ref_str1(
    ref_str1: str = Query(..., description="REF_STR1 값"),
    session: AsyncSession = Depends(get_db_session),
) -> list[RefCodeResponse]:
    """REF_STR1로 MAIN_CODE를 찾아 SUB_CODE, CODE_NAME 조회 (SUB_CODE <> '$' 제외)."""
    sub_query = select(BaseCode.main_code).where(BaseCode.ref_str1 == ref_str1).scalar_subquery()

    result = await session.execute(
        select(BaseCode.sub_code, BaseCode.code_name)
        .where(BaseCode.main_code == sub_query)
        .where(BaseCode.sub_code != "$")
        .where(func.isnull(BaseCode.use_yn, "Y") == "Y"),
    )
    rows = result.all()

    return [RefCodeResponse(sub_code=row.sub_code, code_name=row.code_name) for row in rows]


@router.get("/{main_code}", response_model=list[SubCodeResponse])
async def get_sub_codes(
    main_code: str,
    session: AsyncSession = Depends(get_db_session),
) -> list[SubCodeResponse]:
    """MAIN_CODE 조건으로 코드 목록 조회."""
    result = await session.execute(
        select(BaseCode).where(BaseCode.main_code == main_code),
    )
    rows = result.scalars().all()

    return [SubCodeResponse.model_validate(row) for row in rows]


@router.post("")
async def create_base_code(
    body: BaseCodeCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """BASE_CODE 신규 등록."""
    sql = text(
        "INSERT INTO TB_BASE_CODE ("
        "  MAIN_CODE, SUB_CODE, CODE_NAME,"
        "  REF_NUM1, REF_NUM2, REF_NUM3,"
        "  REF_STR1, REF_STR2, REF_STR3,"
        "  USE_YN, UP_CODE, CODE_LVL, C_LOCK,"
        "  CRE_USER, CRE_DT"
        ") VALUES ("
        "  :main_code, :sub_code, :code_name,"
        "  :ref_num1, :ref_num2, :ref_num3,"
        "  :ref_str1, :ref_str2, :ref_str3,"
        "  :use_yn, '00', '2', 'N',"
        "  :cre_user, GETDATE()"
        ")"
    )
    await session.execute(
        sql,
        {
            "main_code": body.main_code,
            "sub_code": body.sub_code,
            "code_name": body.code_name,
            "ref_num1": body.ref_num1,
            "ref_num2": body.ref_num2,
            "ref_num3": body.ref_num3,
            "ref_str1": body.ref_str1,
            "ref_str2": body.ref_str2,
            "ref_str3": body.ref_str3,
            "use_yn": body.use_yn,
            "cre_user": body.cre_user,
        },
    )
    await session.commit()
    return {"message": "등록되었습니다.", "main_code": body.main_code, "sub_code": body.sub_code}


@router.put("/{main_code}/{sub_code}")
async def update_base_code(
    main_code: str,
    sub_code: str,
    body: BaseCodeUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """BASE_CODE 수정 (MAIN_CODE + SUB_CODE 조건)."""
    result = await session.execute(
        select(BaseCode)
        .where(BaseCode.main_code == main_code)
        .where(BaseCode.sub_code == sub_code),
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="코드를 찾을 수 없습니다.")

    values = {k: v for k, v in body.model_dump().items() if v is not None}

    await session.execute(
        update(BaseCode)
        .where(BaseCode.main_code == main_code)
        .where(BaseCode.sub_code == sub_code)
        .values(**values),
    )
    await session.commit()

    return {"message": "수정되었습니다.", "main_code": main_code, "sub_code": sub_code}
