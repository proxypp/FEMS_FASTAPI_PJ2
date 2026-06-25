from pydantic import BaseModel


class ProdOrderPredResponse(BaseModel):
    """Production order usage prediction response schema (작업지시별 사용예측)."""

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
    unit_used: float | None = None
    pred_qty: float | None = None
    order_unit: str | None = None
    order_state: str | None = None
    last_yn: str | None = None

    model_config = {"from_attributes": True}
