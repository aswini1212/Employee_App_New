"""
Address entity — ORM mapped class for table `address`.
"""

from models.entity import Entity

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.employee import Employee


class Address(Entity):
    __tablename__ = "address"
    __abstract__ = False

    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    employee: Mapped["Employee"] = relationship("Employee", back_populates="addresses")
