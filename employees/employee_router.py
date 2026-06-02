from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
import employees.employee_service as employee_service
from employees.schemas import (
    AddressResponse,
    AssociationResponse,
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
    AddressUpdate,
)
from auth.dependancies import get_current_user, require_role
from models.employee import EmployeeRole

router = APIRouter(prefix="/employee", dependencies=[Depends(get_current_user)])


# creating employee with address
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    tags=["Employees"],
    response_model=EmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create_employee(
    body: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
):
    name = body.name
    email = body.email
    age = body.age
    password = body.password
    addresses = body.addresses
    role = body.role
    employee = await employee_service.create(
        db, name, email, age, password, role, addresses
    )
    # print("employee - ", employee)
    return employee


# getting an employee by name
@router.get("", tags=["Employees"], response_model=EmployeeResponse)
async def get_by_name(name: str, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.get_by_name(name=name, db=db)
    return employee


# getting all the employees
@router.get(
    "",
    tags=["Employees"],
    response_model=list[EmployeeResponse],
)
async def fetch_all(
    db: AsyncSession = Depends(get_db),
):
    result = await employee_service.fetch_all(db)
    return result


# getting an employee with id
@router.get(
    "/id/{emp_id}",
    tags=["Employees"],
    response_model=EmployeeResponse,
)
async def fetch_one(
    emp_id: int,
    db: AsyncSession = Depends(get_db),
    # _current_user: TokenPayload = Depends(get_current_user),
):
    employee = await employee_service.fetch_one(emp_id=emp_id, db=db)
    return employee


# modifying an employee w/o address
@router.put(
    "/{emp_id}",
    tags=["Employees"],
    response_model=EmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update(body: EmployeeUpdate, emp_id: int, db: AsyncSession = Depends(get_db)):
    name = body.name
    email = body.email
    age = body.age
    password = body.password
    employee = await employee_service.update(emp_id, db, name, email, age, password)
    return employee


# modifying an employee with address
@router.put(
    "/{emp_id}/addresses/{address_id}",
    tags=["Employees-Address"],
    response_model=AddressResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update_empaddress(
    body: AddressUpdate,
    emp_id: int,
    address_id: int,
    db: AsyncSession = Depends(get_db),
):
    address = await employee_service.update_empaddress(body, emp_id, address_id, db)
    return address


# deleting an employee with id
@router.delete(
    "/{emp_id}",
    tags=["Employees"],
    response_model=EmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def remove(emp_id: int, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.remove(emp_id, db)
    return employee


# deleting an employee with address
@router.delete(
    "/{emp_id}/adresses/{address_id}",
    tags=["Employees-Address"],
    response_model=AddressResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def remove_empaddress(
    emp_id: int, address_id: int, db: AsyncSession = Depends(get_db)
):
    address = await employee_service.remove_empaddress(emp_id, address_id, db)
    return address


# creating an employee with employee id and department id
@router.post(
    "/{emp_id}/departments/{department_id}",
    tags=["Employee-Department Association"],
    response_model=AssociationResponse,
)
async def create_empdept(
    emp_id: int, department_id: int, db: AsyncSession = Depends(get_db)
):
    association = await employee_service.create_empdept(emp_id, department_id, db)
    return association


# deleting an employee with employee id and department id
@router.delete(
    "/{emp_id}/departments/{department_id}",
    tags=["Employee-Department Association"],
    response_model=AssociationResponse,
)
async def detach_empdept(
    emp_id: int, department_id: int, db: AsyncSession = Depends(get_db)
):
    association = await employee_service.create_empdept(emp_id, department_id, db)
    return association
