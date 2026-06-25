from datetime import datetime

from pydantic import BaseModel


class EquipAlarmResponse(BaseModel):
    """경보알람 조회 결과 (USP_EQUIP_ALARM - TB_PLC_ALARM)."""

    equip_id: str | None = None  # 설비 ID
    equip_name: str | None = None  # 설비명
    meter_id: str | None = None  # 계측기 ID
    meter_name: str | None = None  # 계측기명
    log_dt: str | None = None  # 로그 일자
    log_seq: int | None = None  # 로그 순번
    alarm_state1: int | None = None  # 경보 상태1
    alarm_state2: int | None = None  # 경보 상태2
    alarm_state3: int | None = None  # 경보 상태3
    alarm_state4: int | None = None  # 경보 상태4
    alarm_state5: int | None = None  # 경보 상태5
    log_dtm: datetime | None = None  # 로그 일시

    model_config = {"from_attributes": True}
