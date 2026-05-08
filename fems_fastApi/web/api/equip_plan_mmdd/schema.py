from pydantic import BaseModel, Field


class EquipPlanMmddResponse(BaseModel):
    """월일간 설비점검계획 조회 결과 (USP_EQUIP_PLAN_MMDD - GRID_GBN='M', DML_GBN='S')."""

    mill_cd: str | None = Field(None, alias="MILL_CD")
    plan_year: str | None = Field(None, alias="PLAN_YEAR")
    plan_month: str | None = Field(None, alias="PLAN_MONTH")
    equip_code: str | None = Field(None, alias="EQUIP_CODE")
    d01: str | None = Field(None, alias="D01")
    d02: str | None = Field(None, alias="D02")
    d03: str | None = Field(None, alias="D03")
    d04: str | None = Field(None, alias="D04")
    d05: str | None = Field(None, alias="D05")
    d06: str | None = Field(None, alias="D06")
    d07: str | None = Field(None, alias="D07")
    d08: str | None = Field(None, alias="D08")
    d09: str | None = Field(None, alias="D09")
    d10: str | None = Field(None, alias="D10")
    d11: str | None = Field(None, alias="D11")
    d12: str | None = Field(None, alias="D12")
    d13: str | None = Field(None, alias="D13")
    d14: str | None = Field(None, alias="D14")
    d15: str | None = Field(None, alias="D15")
    d16: str | None = Field(None, alias="D16")
    d17: str | None = Field(None, alias="D17")
    d18: str | None = Field(None, alias="D18")
    d19: str | None = Field(None, alias="D19")
    d20: str | None = Field(None, alias="D20")
    d21: str | None = Field(None, alias="D21")
    d22: str | None = Field(None, alias="D22")
    d23: str | None = Field(None, alias="D23")
    d24: str | None = Field(None, alias="D24")
    d25: str | None = Field(None, alias="D25")
    d26: str | None = Field(None, alias="D26")
    d27: str | None = Field(None, alias="D27")
    d28: str | None = Field(None, alias="D28")
    d29: str | None = Field(None, alias="D29")
    d30: str | None = Field(None, alias="D30")
    d31: str | None = Field(None, alias="D31")

    model_config = {"from_attributes": True, "populate_by_name": True}


class EquipPlanMmddSaveRequest(BaseModel):
    """월일간 설비점검계획 등록/수정 요청 (USP_EQUIP_PLAN_MMDD - DML_GBN='A')."""

    mill_cd: str = ""
    yyyy: str = ""
    mm: str = ""
    dd: str = ""
    equip_code: str = ""
    cre_user: str = ""


class EquipPlanMmddDeleteRequest(BaseModel):
    """월일간 설비점검계획 삭제 요청 (USP_EQUIP_PLAN_MMDD - DML_GBN='D')."""

    mill_cd: str
    yyyy: str
    mm: str
    equip_code: str
