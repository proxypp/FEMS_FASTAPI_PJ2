from datetime import datetime

from pydantic import BaseModel


class BaseFileResponse(BaseModel):
    file_id: str | None = None
    file_gbn: str | None = None
    file_name: str | None = None
    file_ext: str | None = None
    file_size: int | None = None
    cre_user: str | None = None
    cre_dt: datetime | None = None
    upd_user: str | None = None
    upd_dt: datetime | None = None

    model_config = {"from_attributes": True}
