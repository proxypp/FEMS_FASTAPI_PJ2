from pydantic import BaseModel


class BaseCodeCreateRequest(BaseModel):
    """Base code create request schema."""

    main_code: str
    sub_code: str
    code_name: str
    ref_num1: float = 0
    ref_num2: float = 0
    ref_num3: float = 0
    ref_str1: str = ""
    ref_str2: str = ""
    ref_str3: str = ""
    use_yn: str = "Y"
    cre_user: str = ""


class BaseCodeUpdateRequest(BaseModel):
    """Base code update request schema."""

    use_yn: str | None = None
    code_name: str | None = None
    ref_num1: float | None = None
    ref_num2: float | None = None
    ref_num3: float | None = None
    ref_str1: str | None = None
    ref_str2: str | None = None
    ref_str3: str | None = None
    remark: str | None = None


class BaseCodeResponse(BaseModel):
    """Base code response schema."""

    main_code: str
    code_name: str | None = None

    model_config = {"from_attributes": True}


class RefCodeResponse(BaseModel):
    """Ref code response schema."""

    sub_code: str | None = None
    code_name: str | None = None

    model_config = {"from_attributes": True}


class SubCodeResponse(BaseModel):
    """Sub code response schema."""

    main_code: str
    sub_code: str | None = None
    code_name: str | None = None
    ref_num1: float | None = None
    ref_num2: float | None = None
    ref_num3: float | None = None
    ref_str1: str | None = None
    ref_str2: str | None = None
    ref_str3: str | None = None
    use_yn: str | None = None
    remark: str | None = None

    model_config = {"from_attributes": True}
