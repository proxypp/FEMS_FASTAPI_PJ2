from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.user import User
from fems_fastApi.services.auth.jwt import create_access_token
from fems_fastApi.services.auth.password import hash_password, verify_password
from fems_fastApi.web.api.auth.schema import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """User login endpoint."""
    # 1. DB에서 유저 조회
    result = await session.execute(
        select(User).where(User.user_id == body.user_id),
    )
    user = result.scalar_one_or_none()

    # 2. 유저 존재 여부 + 비밀번호 검증
    if not user or not verify_password(body.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. 계정 활성화 여부 확인
    if user.use_yn != "Y" or user.del_yn == "Y":
        raise HTTPException(status_code=403, detail="Account is disabled")

    # 4. 마지막 로그인 시간 업데이트
    await session.execute(
        update(User)
        .where(User.user_id == body.user_id)
        .values(last_login=datetime.now(timezone.utc)),
    )

    # 5. JWT 토큰 생성 및 반환
    token = create_access_token(user.user_id)
    return TokenResponse(
        access_token=token,
        user_id=user.user_id,
        user_nm=user.user_nm,
        admin_yn=user.admin_yn,
    )

@router.post("/register", response_model=RegisterResponse)
async def register(
    body: RegisterRequest,
    session: AsyncSession = Depends(get_db_session),
) -> RegisterResponse:
    """User register endpoint."""
    # 1. 아이디 중복 확인
    result = await session.execute(
        select(User).where(User.user_id == body.user_id),
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User ID already exists")

    # 2. 유저 생성
    user = User(
        user_id=body.user_id,
        password=hash_password(body.password),
        user_nm=body.user_nm,
        email=body.email,
        hp_no=body.hp_no,
        company=body.company,
        password_update_date=datetime.now(timezone.utc),
    )
    session.add(user)
    await session.flush()

    return RegisterResponse(user_id=body.user_id)