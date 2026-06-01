"""
Department entity — ORM mapped class for table `department`.
"""

from datetime import datetime
from typing import Any

# from models.emp_dep_assoc import Emp_Dept_Assoc
# from models.employee import Employee
from models.emp_dep_assoc import Emp_Dept_Assoc
from models.entity import Entity

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Department(Entity):
    __tablename__ = "department"
    __abstract__ = False
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }

    employee_departments: Mapped[list["Emp_Dept_Assoc"]] = relationship(
        "Emp_Dept_Assoc", back_populates="department"
    )
