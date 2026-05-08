from datetime import date

from pydantic import BaseModel, Field


class EquipPlanYymmResponse(BaseModel):
    """년월간 설비점검계획 조회 결과 (USP_EQUIP_PLAN_YYMM - GRID_GBN='M', DML_GBN='S')."""

    mill_cd: str | None = Field(None, alias="MILL_CD")
    equip_code: str | None = Field(None, alias="EQUIP_CODE")
    equip_name: str | None = Field(None, alias="EQUIP_NAME")
    plan_year: str | None = Field(None, alias="PLAN_YEAR")
    plan_date01: date | None = Field(None, alias="1")
    plan_date02: date | None = Field(None, alias="2")
    plan_date03: date | None = Field(None, alias="3")
    plan_date04: date | None = Field(None, alias="4")
    plan_date05: date | None = Field(None, alias="5")
    plan_date06: date | None = Field(None, alias="6")
    plan_date07: date | None = Field(None, alias="7")
    plan_date08: date | None = Field(None, alias="8")
    plan_date09: date | None = Field(None, alias="9")
    plan_date10: date | None = Field(None, alias="10")
    plan_date11: date | None = Field(None, alias="11")
    plan_date12: date | None = Field(None, alias="12")

    model_config = {"from_attributes": True, "populate_by_name": True}


class EquipPlanYymmSaveRequest(BaseModel):
    """년월간 설비점검계획 등록/수정 요청 (USP_EQUIP_PLAN_YYMM - DML_GBN='A')."""

    mill_cd: str = ""
    plan_year: str = ""
    equip_code: str = ""
    plan_date01: date | None = None
    plan_date02: date | None = None
    plan_date03: date | None = None
    plan_date04: date | None = None
    plan_date05: date | None = None
    plan_date06: date | None = None
    plan_date07: date | None = None
    plan_date08: date | None = None
    plan_date09: date | None = None
    plan_date10: date | None = None
    plan_date11: date | None = None
    plan_date12: date | None = None
    cre_user: str = ""
    upd_user: str = ""


class EquipPlanYymmDeleteRequest(BaseModel):
    """년월간 설비점검계획 삭제 요청 (USP_EQUIP_PLAN_YYMM - DML_GBN='D')."""

    mill_cd: str
    equip_code: str
    plan_year: str
