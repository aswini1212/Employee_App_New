from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from exceptions import ConflictException, NotFoundException
from models import Department
from models.emp_dep_assoc import Emp_Dept_Assoc


# creating a department
async def create(db: AsyncSession, name: str):
    department = Department(name=name.strip())
    db.add(department)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        print(e)
        raise
    await db.refresh(department)
    return department


# fetching all the departments
async def fetch_all(db: AsyncSession):
    stmt = select(Department).where(Department.deleted_at.is_(None))
    department = await db.scalars(stmt)
    if not department:
        raise NotFoundException(detail="Department not found")
    return department


# fetching one department with employees
async def fetch_one(dept_id: int, db: AsyncSession):
    # to avoild lazy loading we are using select in load---load the departments, then the association rows and then the employees
    stmt = (
        select(Department)
        .options(
            selectinload(Department.employee_departments).selectinload(
                Emp_Dept_Assoc.employee
            )
        )
        .where(Department.deleted_at.is_(None))
        .where(Department.id == dept_id)
    )
    result = await db.scalars(stmt)
    department = result.first()
    if not department:
        raise NotFoundException(detail="Department not found")
    return department


# updating a department
async def update(dept_id: int, db: AsyncSession, name: str):
    department = await fetch_one(dept_id, db)
    department.name = name

    if not department:
        raise NotFoundException(detail="Department not found")
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        print(e)
        raise

    await db.refresh(department)
    return department


# removing a department
async def remove(dept_id: int, db: AsyncSession):
    department = await fetch_one(dept_id, db)
    department.deleted_at = datetime.now()
    if not department:
        raise NotFoundException(detail="Department not found")
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Email already in use")
    await db.refresh(department)
    return department
