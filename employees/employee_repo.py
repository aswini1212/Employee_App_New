from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from employees.schemas import AddressUpdate
from exceptions import ConflictException, NotFoundException
from models import Employee, Address
from models.emp_dep_assoc import Emp_Dept_Assoc
from models.employee import EmployeeRole
import logging

logger = logging.getLogger(__name__)


# creating an employee with address
async def create(
    db: AsyncSession,
    name: str,
    email: str,
    age: int,
    password: str,
    role: EmployeeRole,
    addresses,
):
    db_employee = Employee(
        name=name.strip(),
        email=email.strip(),
        age=age,
        password_hash=password,
        role=role,
    )
    if addresses:
        for addr in addresses:
            db_employee.addresses.append(
                Address(
                    line1=addr.line1,
                    city=addr.city,
                    postal_code=addr.postal_code,
                    country=addr.country,
                )
            )
    db.add(db_employee)

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        print(e)
        raise
    await db.refresh(db_employee)
    # to overcome the problem of greenlet error caused due to lazy loading we areexplicitly loading the employees with addresses again
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.id == db_employee.id)
    )
    result = await db.scalars(stmt)
    db_employee = result.first()
    return db_employee


# getting all the employees with adresses
async def fetch_all(db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.deleted_at.is_(None))
    )
    db_employee = await db.scalars(stmt)
    if not db_employee:
        raise NotFoundException(detail="Employee not found")
    return db_employee


# getting one employee with address
async def fetch_one(emp_id: int, db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.deleted_at.is_(None))
        .where(Employee.id == emp_id)
    )
    db_employee = await db.scalars(stmt)
    emp = db_employee.first()
    if not emp:
        logger.info("ERROR: employee has not been fetched successfully")
        raise NotFoundException(detail="Employee not found")
    return emp


# getting an employee by name
async def get_by_name(name: str, db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.deleted_at.is_(None))
        .where(Employee.name.like(f"%{name}%"))
    )
    emp = await db.scalars(stmt)
    db_employee = emp.first()
    if not db_employee:
        raise NotFoundException(detail="Employe not found")
    return db_employee


# getting an employee by email
async def get_by_email(email: str, db: AsyncSession) -> Employee | None:
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.email == email)
        .where(Employee.deleted_at.is_(None))
    )
    result = await db.scalars(stmt)
    db_employee = result.first()
    if not db_employee:
        raise NotFoundException(detail="Employee not found")
    return db_employee


# updating an employee w/o address
async def update(
    emp_id: int, db: AsyncSession, name: str, email: str, age: int, password: str
):
    db_employee = await fetch_one(emp_id, db)
    if not db_employee:
        raise NotFoundException(detail="Employee not found")
    db_employee.name = name
    db_employee.email = email
    db_employee.age = age
    db_employee.password_hash = password

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Email already in use")
    await db.refresh(db_employee)
    return db_employee


# updating the address of an employee
async def update_empaddress(
    body: AddressUpdate, emp_id: int, address_id: int, db: AsyncSession
):
    stmt = (
        select(Address)
        .where(Address.id == address_id)
        .where(Address.employee_id == emp_id)
    )
    result = await db.scalars(stmt)
    address = result.first()
    if not address:
        raise NotFoundException("Address not found")

    address.line1 = body.line1
    address.city = body.city
    address.postal_code = body.postal_code
    address.country = body.country

    await db.commit()
    await db.refresh(address)

    return address


# removing an employee
async def remove(emp_id: int, db: AsyncSession):
    db_employee = await fetch_one(emp_id, db)
    db_employee.deleted_at = datetime.now()
    if not db_employee:
        raise NotFoundException(detail="Employe not found")
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Email already in use")
    await db.refresh(db_employee)
    return db_employee


# removing an the address of an employee
async def remove_empaddress(emp_id, address_id, db):
    db_employee = await fetch_one(emp_id, db)
    # loop to identify which address needs to be removed depending on the id passed
    address = next(
        (
            addr
            for addr in db_employee.addresses
            if addr.id == address_id and addr.deleted_at is None
        ),
        None,
    )

    address.deleted_at = datetime.now()
    await db.commit()
    await db.refresh(db_employee)
    return address


# attaching an employee to a department in assoc
async def create_empdept(emp_id: int, department_id: int, db: AsyncSession):
    association = Emp_Dept_Assoc(employee_id=emp_id, department_id=department_id)
    db.add(association)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(association)
    return association


# detaching an employee from a department in assoc
async def detach_empdept(emp_id: int, department_id: int, db: AsyncSession):
    stmt = (
        select(Emp_Dept_Assoc)
        .where(Emp_Dept_Assoc.employee_id == emp_id)
        .where(Emp_Dept_Assoc.department_id == department_id)
        .where(Emp_Dept_Assoc.deleted_at.is_(None))
    )
    result = await db.scalars(stmt)
    association = result.first()

    if not association:
        raise NotFoundException(detail="Association not found")

    association.deleted_at = datetime.now()

    await db.commit()
    await db.refresh(association)

    return association
