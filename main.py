from fastapi import FastAPI

import logging


from exceptions.handlers import register_exception_handlers
from middleware import configure_middleware


from employees.employee_router import router as employee_router
from departments.department_router import router as department_router


from auth.router import router as auth_router

# middleware functionality for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="Employee App",
    description="Employee app which shows details abot the employees, departments they work in and the addresses of employees",
)

# MIDDLEWARE
configure_middleware(app)

# ROUTERS
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(auth_router)

# GLOBAL EXCEPTION HANDLING
# @app.exception_handler(NotFoundException)
# async def not_found_exception(request: Request, exc: NotFoundException):
#     return JSONResponse(
#         status_code=404,
#         content={"detail":"Employee is not found: from global expection handler"},
#     )

register_exception_handlers(app)

# POST EMPLOYEE
# @app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee = Employee(name=name.strip(), email=email.strip())
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

# GET ALL EMPLOYEES
# @app.get("/employee", tags=["Employees"])
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     return [r.to_api_dict() for r in result.all()]

# GET ONE EMPLOYEE
# @app.get("/employee/{emp_id}",tags=["Employees"])
# async def display_one_employee(emp_id:int,db: AsyncSession = Depends(get_db)):
#     stmt=select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id==emp_id)
#     result = await db.scalars(stmt)
#     return [r.to_api_dict() for r in result.all()]


# UPDATE ALL EMPLOYEES
# @app.put("/employee/{emp_id}",tags=["Employees"])
# async def update_one_employee(emp_id:int, body: dict = Body(...),db: AsyncSession = Depends(get_db)):
#     stmt=select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id==emp_id)
#     result = await db.scalars(stmt)
#     name=body.get("name")
#     email=body.get("email")
#     db_employee = result.first()
#     if not db_employee:
#         raise HTTPException(status_code=404,detail="Employee not found")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")

#     db_employee.name=name
#     db_employee.email=email

#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")

#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()

# DELETE ONE EMPLOYEE
# @app.delete("/employee/{emp_id}")
# async def emp_delete(emp_id:int, db: AsyncSession = Depends(get_db)):
#     stmt=select(Employee).where(Employee.deleted_at.is_(None)).where(Employee.id==emp_id)
#     result= await db.scalars(stmt)
#     db_employee= result.first()
#     db_employee.deleted_at=datetime.now()
#     if not db_employee:
#         raise HTTPException(status_code=404,detail="Employee not found")

#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")

#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()


# @app.get("/health", tags=["Health"])
# def health_check():
#     return {"status": "healthy", "env": settings.app_env}
