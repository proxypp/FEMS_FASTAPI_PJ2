from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.user import User
from fems_fastApi.services.auth.jwt import create_access_token
from fems_fastApi.web.api.auth.schema import (
    LoginRequest,
    LogoutRequest,
    TokenResponse,
)
router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
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
    # if not user or not verify_password(body.password, user.password):
    if not user or user.password != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. 계정 활성화 여부 확인
    if user.use_yn != "Y":
        raise HTTPException(status_code=403, detail="Account is disabled")

    # 4. 로그인 시간 및 IP 업데이트
    await session.execute(
        update(User)
        .where(User.user_id == body.user_id)
        .values(
            login_dt=datetime.now(KST),
            ip_addr=request.client.host,
        ),
    )
    await session.commit()

    # 5. 로그인 성공 응답
    return TokenResponse(
        access_token=create_access_token(user.user_id),
        user_id=user.user_id,
        user_nm=user.user_nm,
        admin_yn=user.admin_yn,
    )


@router.post("/logout")
async def logout(
    body: LogoutRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """User logout endpoint."""
    result = await session.execute(select(User).where(User.user_id == body.user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    await session.execute(
        update(User)
        .where(User.user_id == body.user_id)
        .values(logout_dt=datetime.now(KST)),
    )
    await session.commit()

    return {"message": "로그아웃되었습니다.", "user_id": body.user_id}

