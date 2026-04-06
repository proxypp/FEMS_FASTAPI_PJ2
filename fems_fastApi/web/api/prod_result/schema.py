from pydantic import BaseModel


class ProdResultResponse(BaseModel):
    """Production result response schema."""

    mill_cd: str | None = None
    order_no: str | None = None
    sub_order: float | None = None
    rout_seq: float | None = None
    work_seq: float | None = None
    rout_code: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    item_code: str | None = None
    item_name: str | None = None
    start_dt: str | None = None
    prod_qty: float | None = None
    bad_qty: float | None = None
    order_unit: str | None = None
    work_state: str | None = None
    last_yn: str | None = None

    model_config = {"from_attributes": True}


class ProdResultSaveRequest(BaseModel):
    """Production result save (insert/update) request schema."""

    mill_cd: str = "1"
    start_dt: str
    order_no: str
    sub_order: int
    rout_seq: int
    work_seq: int | None = None
    rout_code: str | None = None
    equip_code: str | None = None
    item_code: str | None = None
    prod_qty: int | None = None
    bad_qty: int | None = None
    cre_user: str | None = None
    upd_user: str | None = None


class ProdResultDeleteRequest(BaseModel):
    """Production result delete request schema."""

    order_no: str
    sub_order: int
    rout_seq: int
    work_seq: int
