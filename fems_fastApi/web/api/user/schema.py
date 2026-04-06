from datetime import datetime

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    """User create request schema."""

    # 입력 필수
    user_id: str
    user_nm: str
    user_pw: str
    # 입력값 (선택)
    tel: str | None = None
    use_dt: str | None = None
    # 기본값 있는 필드
    mill_cd: str = "1"
    plant_code: str = "01"
    use_yn: str = "Y"
    admin_yn: str = "N"
    cre_user: str = "swit"
    # NULL로 INSERT
    login_dt: None = None
    logout_dt: None = None
    login_status: None = None
    ip_addr: None = None
    upd_user: None = None
    upd_dt: None = None


class UserUpdateRequest(BaseModel):
    """User update request schema."""

    user_nm: str | None = None
    plant_code: str | None = None
    tel: str | None = None
    use_yn: str | None = None


class UserResponse(BaseModel):
    """User response schema."""

    mill_cd: str | None = None
    user_id: str
    plant_code: str | None = None
    user_nm: str | None = None
    tel: str | None = None
    login_dt: datetime | None = None
    logout_dt: datetime | None = None
    login_status: str | None = None
    ip_addr: str | None = None
    use_dt: str | None = None
    use_yn: str | None = None
    admin_yn: str | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}


class UserMenuPermissionSaveRequest(BaseModel):
    """사용자 메뉴 권한 저장 요청 스키마."""

    menu_id: str
    parent_id: str | None = None
    use_yn: str = "N"


class UserMenuPermissionUpdateRequest(BaseModel):
    """사용자 메뉴 권한 수정 요청 스키마."""

    use_yn: str
    upd_user: str


class UserMenuPermissionResponse(BaseModel):
    """사용자 메뉴 사용 권한 응답 스키마."""

    menu_id: str
    menu_name: str | None = None
    parent_id: str | None = None
    use_yn: str
    user_id: str | None = None
