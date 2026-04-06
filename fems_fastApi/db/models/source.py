from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from fems_fastApi.db.base import Base


class Source(Base):
    """Source model for TB_FEMS_SOURCE."""

    __tablename__ = "TB_FEMS_SOURCE"
    __table_args__ = {"schema": "dbo"}

    mill_cd: Mapped[str | None] = mapped_column("MILL_CD", String(5), nullable=True)
    plant_code: Mapped[str | None] = mapped_column("PLANT_CODE", String(50), nullable=True)
    plant_name: Mapped[str | None] = mapped_column("PLANT_NAME", String(50), nullable=True)
    source_id: Mapped[str] = mapped_column("SOURCE_ID", String(50), primary_key=True)
    source_name: Mapped[str | None] = mapped_column("SOURCE_NAME", String(50), nullable=True)
    unit: Mapped[str | None] = mapped_column("UNIT", String(50), nullable=True)
    energy_type: Mapped[str | None] = mapped_column("ENERGY_TYPE", String(50), nullable=True)
    energy_type_name: Mapped[str | None] = mapped_column("ENERGY_TYPE_NAME", String(50), nullable=True)
    use_yn: Mapped[str | None] = mapped_column("USE_YN", String(100), nullable=True)
    cre_user: Mapped[str | None] = mapped_column("CRE_USER", String(50), nullable=True)
    cre_dt: Mapped[datetime | None] = mapped_column("CRE_DT", DateTime, server_default=func.now())
    upd_user: Mapped[str | None] = mapped_column("UPD_USER", String(50), nullable=True)
    upd_dt: Mapped[datetime | None] = mapped_column("UPD_DT", DateTime, nullable=True)
