from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException
from models.department import Department
import departments.department_repo as department_repo


# creating a department
async def create(db: AsyncSession, name: str) -> Department:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException(detail="name must be a non-empty string")

    department = await department_repo.create(db, name)
    return department


# fetching all the departments
async def fetch_all(db: AsyncSession) -> Department:
    department = await department_repo.fetch_all(db)
    return department


# fetching one department with employees
async def fetch_one(dept_id: int, db: AsyncSession) -> Department:
    result = await department_repo.fetch_one(dept_id, db)
    department = {
        "name": result.name,
        "employees": [assoc.employee for assoc in result.employee_departments],
    }
    return department


# updating a department
async def update(dept_id: int, db: AsyncSession, name: str) -> Department:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException(detail="name must be a non-empty string")

    department = await department_repo.update(dept_id, db, name)
    return department


# removing a department
async def remove(dept_id: int, db: AsyncSession) -> Department:
    department = await department_repo.remove(dept_id, db)
    if not department:
        raise NotFoundException(detail="Department not found")
    return department
