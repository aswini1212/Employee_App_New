from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import BadRequestException, NotFoundException
from models.address import Address
from models.employee import Employee, EmployeeRole
import employees.employee_repo as employee_repo
from auth.utils import hash_password
from employees.schemas import AddressCreate, AddressUpdate


# creating an employee with address
async def create(
    db: AsyncSession,
    name: str,
    email: str,
    age: int,
    password: str,
    role: EmployeeRole,
    addresses: list[AddressCreate],
) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException(detail="name must be a non-empty string")

    if not isinstance(email, str) or not email.strip():
        raise BadRequestException(detail="email must be a non-empty string")

    hashed = hash_password(password)
    employee = await employee_repo.create(
        db=db,
        name=name,
        email=email,
        age=age,
        password=hashed,
        addresses=addresses,
        role=role,
    )
    # print("here - ", employee)
    return employee


# getting all the employees with adresses
async def fetch_all(db: AsyncSession) -> Employee:
    employee = await employee_repo.fetch_all(db)
    return employee


# getting one employee with address
async def fetch_one(emp_id: int, db: AsyncSession) -> Employee:
    employee = await employee_repo.fetch_one(emp_id, db)
    return employee


# getting an employee by name
async def get_by_name(name: str, db: AsyncSession):
    employee = await employee_repo.get_by_name(name, db)
    return employee


# updating an employee
async def update(
    emp_id: int, db: AsyncSession, name: str, email: str, age: int, password: str
) -> Employee:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException(detail="name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException(detail="email must be a non-empty string")
    hashed = hash_password(password)
    employee = await employee_repo.update(emp_id, db, name, email, age, hashed)
    return employee


# updating the address of an employee
async def update_empaddress(
    body: AddressUpdate, emp_id: int, address_id: int, db: AsyncSession
) -> Address:
    address = await employee_repo.update_empaddress(body, emp_id, address_id, db)
    return address


# removing an employee
async def remove(emp_id: int, db: AsyncSession) -> Employee:
    employee = await employee_repo.remove(emp_id, db)
    if not employee:
        raise NotFoundException(detail="Employee not found")
    return employee


# removing an the address of an employee
async def remove_empaddress(emp_id: int, address_id: int, db: AsyncSession) -> Address:
    address = await employee_repo.remove_empaddress(emp_id, address_id, db)
    if not address:
        raise NotFoundException(detail="Address not found")
    return address


# attaching dept and emp_id to assoc table
async def create_empdept(emp_id: int, department_id: int, db: AsyncSession):
    association = await employee_repo.create_empdept(emp_id, department_id, db)
    if not association:
        raise NotFoundException("Association not found between employee and department")
    return association


# detaching dept and emp_id to assoc table
async def detach_empdept(emp_id: int, department_id: int, db: AsyncSession):
    association = await employee_repo.create_empdept(emp_id, department_id, db)
    if not association:
        raise NotFoundException("Association not found between employee and department")
    return association
