"""
Address entity — ORM mapped class for table `address`.
"""

from datetime import datetime
from typing import Any, Optional

from models.entity import Entity

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

from typing import TYPE_CHECKING
#to resolve cyclic imports
if TYPE_CHECKING:
    from models.employee import Employee
    from models.department import Department


class Emp_Dept_Assoc(Entity):
    __tablename__="emp_dep_assoc"
    __abstract__=False

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("department.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    employee: Mapped["Employee"] = relationship("Employee", back_populates="employee_departments")
    department: Mapped["Department"] = relationship("Department", back_populates="employee_departments")
    

