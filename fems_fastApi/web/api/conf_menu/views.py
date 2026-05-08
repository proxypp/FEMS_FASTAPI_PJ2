from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from fems_fastApi.db.dependencies import get_db_session
from fems_fastApi.web.api.conf_menu.schema import (
    MainMenuCreateRequest,
    MenuResponse,
    MenuSubResponse,
    MenuUpdateRequest,
    SubMenuCreateRequest,
)

router = APIRouter()


@router.get("/main", response_model=list[MenuResponse])
async def get_main_menus(
    session: AsyncSession = Depends(get_db_session),
) -> list[MenuResponse]:
    """메인 메뉴 목록 조회 (PARENT_ID = '0')."""
    result = await session.execute(
        text("SELECT MENU_ID, MENU_NAME, PARENT_ID FROM TB_CONF_MENU WHERE PARENT_ID = '0' ORDER BY DISSORT"),
    )
    rows = result.mappings().all()
    return [MenuResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.get("/sub", response_model=list[MenuSubResponse])
async def get_sub_menus(
    menu_id: str = Query(..., description="상위 메뉴 ID"),
    session: AsyncSession = Depends(get_db_session),
) -> list[MenuSubResponse]:
    """서브 메뉴 목록 조회 (PARENT_ID = menu_id, USE_YN = 'Y')."""
    result = await session.execute(
        text(
            "SELECT MENU_ID, MENU_NAME, USE_YN"
            " FROM TB_CONF_MENU"
            " WHERE PARENT_ID = :menu_id"
            "   AND ISNULL(USE_YN, 'Y') = 'Y'"
            " ORDER BY DISSORT"
        ),
        {"menu_id": menu_id},
    )
    rows = result.mappings().all()
    return [MenuSubResponse(**{k.lower(): v for k, v in row.items()}) for row in rows]


@router.post("/main")
async def create_main_menu(
    body: MainMenuCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """메인 메뉴 등록 (MENU_TYPE='0', PARENT_ID='0')."""
    await session.execute(
        text(
            "INSERT INTO TB_CONF_MENU"
            " (MENU_ID, MENU_NAME, MENU_TYPE, PARENT_ID, USE_YN, DISSORT, CRE_DT, CRE_USER)"
            " VALUES"
            " (:menu_id, :menu_name, '0', '0', 'Y',"
            "  (SELECT ISNULL(MAX(DISSORT), 0) FROM TB_CONF_MENU),"
            "  GETDATE(), :cre_user)"
        ),
        {"menu_id": body.menu_id, "menu_name": body.menu_name, "cre_user": body.cre_user},
    )
    await session.commit()
    return {"message": "등록되었습니다.", "menu_id": body.menu_id}


@router.post("/sub")
async def create_sub_menu(
    body: SubMenuCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """서브 메뉴 등록 (MENU_TYPE='1', PARENT_ID=parent_id)."""
    await session.execute(
        text(
            "INSERT INTO TB_CONF_MENU"
            " (MENU_ID, MENU_NAME, MENU_TYPE, PARENT_ID, USE_YN, DISSORT, CRE_DT, CRE_USER)"
            " VALUES"
            " (:menu_id, :menu_name, '1', :parent_id, 'Y',"
            "  (SELECT ISNULL(MAX(DISSORT), 0) FROM TB_CONF_MENU),"
            "  GETDATE(), :cre_user)"
        ),
        {
            "menu_id": body.menu_id,
            "menu_name": body.menu_name,
            "parent_id": body.parent_id,
            "cre_user": body.cre_user,
        },
    )
    await session.commit()
    return {"message": "등록되었습니다.", "menu_id": body.menu_id}


@router.put("/{menu_id}")
async def update_menu(
    menu_id: str,
    body: MenuUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """메뉴명 수정."""
    result = await session.execute(
        text("SELECT MENU_ID FROM TB_CONF_MENU WHERE MENU_ID = :menu_id"),
        {"menu_id": menu_id},
    )
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다.")

    await session.execute(
        text(
            "UPDATE TB_CONF_MENU"
            " SET MENU_NAME = :menu_name, UPD_USER = :upd_user, UPD_DT = GETDATE()"
            " WHERE MENU_ID = :menu_id"
        ),
        {"menu_name": body.menu_name, "upd_user": body.upd_user, "menu_id": menu_id},
    )
    await session.commit()
    return {"message": "수정되었습니다.", "menu_id": menu_id}


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """메뉴 삭제."""
    result = await session.execute(
        text("SELECT MENU_ID FROM TB_CONF_MENU WHERE MENU_ID = :menu_id"),
        {"menu_id": menu_id},
    )
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="메뉴를 찾을 수 없습니다.")

    await session.execute(
        text("DELETE FROM TB_CONF_MENU WHERE MENU_ID = :menu_id"),
        {"menu_id": menu_id},
    )
    await session.commit()
    return {"message": "삭제되었습니다.", "menu_id": menu_id}
