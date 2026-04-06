from pydantic import BaseModel


class ProdOrderResponse(BaseModel):
    """Production order response schema."""

    mill_cd: str | None = None
    order_no: str | None = None
    sub_order: float | None = None
    rout_seq: float | None = None
    rout_code: str | None = None
    equip_code: str | None = None
    equip_name: str | None = None
    item_code: str | None = None
    item_name: str | None = None
    order_dt: str | None = None
    order_qty: float | None = None
    order_unit: str | None = None
    order_state: str | None = None
    last_yn: str | None = None

    model_config = {"from_attributes": True}


class ProdOrderDeleteRequest(BaseModel):
    """Production order delete request schema."""

    order_no: str
    sub_order: int
    rout_seq: int


class ProdOrderSaveRequest(BaseModel):
    """Production order save (insert/update) request schema."""

    mill_cd: str = "1"
    order_dt: str
    order_no: str | None = None
    sub_order: int | None = None
    rout_seq: int | None = None
    rout_code: str | None = None
    equip_code: str | None = None
    item_code: str | None = None
    order_qty: int | None = None
    cre_user: str | None = None
    upd_user: str | None = None
