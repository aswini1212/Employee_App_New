"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
import enum
from models.address import Address

# from models.department import Department
from models.emp_dep_assoc import Emp_Dept_Assoc
from models.entity import Entity

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class Employee(Entity):
    __tablename__ = "employees"
    __abstract__ = False

    role: Mapped[EmployeeRole] = mapped_column(
        Enum(
            EmployeeRole,
            name="employeerole",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
    )

    employee_departments: Mapped[list["Emp_Dept_Assoc"]] = relationship(
        "Emp_Dept_Assoc", back_populates="employee"
    )
