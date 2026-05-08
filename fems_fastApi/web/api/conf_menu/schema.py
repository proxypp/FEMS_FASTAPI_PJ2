from pydantic import BaseModel


class MenuResponse(BaseModel):
    """메뉴 조회 응답."""

    model_config = {"from_attributes": True}

    menu_id: str | None = None
    menu_name: str | None = None
    parent_id: str | None = None


class MenuSubResponse(BaseModel):
    """서브 메뉴 조회 응답."""

    model_config = {"from_attributes": True}

    menu_id: str | None = None
    menu_name: str | None = None
    use_yn: str | None = None


class MainMenuCreateRequest(BaseModel):
    """메인 메뉴 등록 요청."""

    menu_id: str
    menu_name: str
    cre_user: str = ""


class SubMenuCreateRequest(BaseModel):
    """서브 메뉴 등록 요청."""

    menu_id: str
    menu_name: str
    parent_id: str
    cre_user: str = ""


class MenuUpdateRequest(BaseModel):
    """메뉴 수정 요청."""

    menu_name: str
    upd_user: str = ""
