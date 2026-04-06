from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.db.models.menu import ConfMenu, ConfUserMenu
from fems_fastApi.db.models.user import User
from fems_fastApi.web.api.user.schema import (
    UserCreateRequest,
    UserMenuPermissionResponse,
    UserMenuPermissionSaveRequest,
    UserMenuPermissionUpdateRequest,
    UserResponse,
    UserUpdateRequest,
)

router = APIRouter()


@router.get("", response_model=list[UserResponse])
async def get_users(
    user_id: str | None = Query(None, description="사용자 ID (부분 검색)"),
    user_nm: str | None = Query(None, description="사용자 명 (부분 검색)"),
    use_yn: str = Query(default="", description="사용여부 (Y: 사용, N: 미사용, 빈값: 전체)"),
    session: AsyncSession = Depends(get_db_session),
) -> list[UserResponse]:
    """사용자 목록 조회."""
    query = select(User)

    if use_yn:
        query = query.where(func.isnull(User.use_yn, "Y") == use_yn)

    if user_id:
        query = query.where(User.user_id.like(f"%{user_id}%"))
    if user_nm:
        query = query.where(User.user_nm.like(f"%{user_nm}%"))

    result = await session.execute(query)
    rows = result.scalars().all()

    return [UserResponse.model_validate(row) for row in rows]


@router.post("", status_code=201)
async def create_user(
    body: UserCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """사용자 등록."""
    result = await session.execute(select(User).where(User.user_id == body.user_id))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="이미 존재하는 사용자 ID입니다.")

    await session.execute(
        insert(User).values(
            mill_cd=body.mill_cd,
            user_id=body.user_id,
            plant_code=body.plant_code,
            user_nm=body.user_nm,
            password=body.user_pw,
            tel=body.tel,
            login_dt=None,
            logout_dt=None,
            login_status=None,
            ip_addr=None,
            use_dt=body.use_dt,
            use_yn=body.use_yn,
            cre_user=body.cre_user,
            upd_user=None,
            upd_dt=None,
            admin_yn=body.admin_yn,
        ),
    )
    await session.commit()

    return {"message": "등록되었습니다.", "user_id": body.user_id}


@router.get("/{user_id}/menus", response_model=list[UserMenuPermissionResponse])
async def get_user_menu_permissions(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> list[UserMenuPermissionResponse]:
    """사용자 메뉴 사용 권한 조회.

    전체 메뉴(MENU_TYPE='1', 활성) 목록을 가져오고,
    해당 사용자의 권한 여부(USE_YN)를 함께 반환합니다.
    권한 정보가 없는 메뉴는 USE_YN='N' 으로 반환됩니다.
    """
    query = (
        select(
            ConfMenu.menu_id,
            ConfMenu.menu_name,
            ConfMenu.parent_id,
            func.isnull(ConfUserMenu.use_yn, "N").label("use_yn"),
            ConfUserMenu.user_id,
        )
        .outerjoin(
            ConfUserMenu,
            and_(
                ConfMenu.menu_id == ConfUserMenu.menu_id,
                ConfUserMenu.user_id == user_id,
            ),
        )
        .where(ConfMenu.menu_type == "1")
        .where(func.isnull(ConfMenu.use_yn, "Y") == "Y")
        .order_by(ConfMenu.dis_sort)
    )

    result = await session.execute(query)
    rows = result.mappings().all()

    return [UserMenuPermissionResponse(**row) for row in rows]


@router.post("/{user_id}/menus", status_code=201)
async def save_user_menu_permissions(
    user_id: str,
    body: list[UserMenuPermissionSaveRequest],
    cre_user: str = Query(default="system", description="등록자 ID"),
    mill_cd: str = Query(default="1", description="밀 코드"),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """사용자 메뉴 권한 저장.

    기존 권한을 삭제 후 전달받은 목록으로 재등록합니다.
    """
    # 기존 권한 삭제
    await session.execute(
        delete(ConfUserMenu).where(ConfUserMenu.user_id == user_id),
    )

    # 신규 권한 일괄 INSERT
    if body:
        await session.execute(
            insert(ConfUserMenu),
            [
                {
                    "mill_cd": mill_cd,
                    "user_id": user_id,
                    "parent_id": item.parent_id,
                    "menu_id": item.menu_id,
                    "use_yn": item.use_yn,
                    "cre_user": cre_user,
                    "upd_user": None,
                    "upd_dt": None,
                }
                for item in body
            ],
        )

    await session.commit()

    return {"message": "권한이 저장되었습니다.", "user_id": user_id, "count": len(body)}


@router.put("/{user_id}/menus/{menu_id}")
async def update_user_menu_permission(
    user_id: str,
    menu_id: str,
    body: UserMenuPermissionUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """사용자 메뉴 권한 수정 (USE_YN)."""
    result = await session.execute(
        select(ConfUserMenu).where(
            and_(
                ConfUserMenu.user_id == user_id,
                ConfUserMenu.menu_id == menu_id,
            ),
        ),
    )
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(status_code=404, detail="권한 정보를 찾을 수 없습니다.")

    await session.execute(
        update(ConfUserMenu)
        .where(
            and_(
                ConfUserMenu.user_id == user_id,
                ConfUserMenu.menu_id == menu_id,
            ),
        )
        .values(
            use_yn=body.use_yn,
            upd_user=body.upd_user,
            upd_dt=func.now(),
        ),
    )
    await session.commit()

    return {"message": "권한이 수정되었습니다.", "user_id": user_id, "menu_id": menu_id}


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    body: UserUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """사용자 정보 수정 (USER_NM, PLANT_CODE, TEL, USE_YN)."""
    result = await session.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    values = {k: v for k, v in body.model_dump().items() if v is not None}

    await session.execute(
        update(User).where(User.user_id == user_id).values(**values),
    )
    await session.commit()

    return {"message": "수정되었습니다.", "user_id": user_id}
