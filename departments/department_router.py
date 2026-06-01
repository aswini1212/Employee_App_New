from fastapi import APIRouter, Depends, Body,status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
import departments.department_service as department_service
from departments.schemas import DepartmentCreate, DepartmentDetailResponse, DepartmentResponse, DepartmentUpdate

router= APIRouter(prefix="/department", tags=["Departments"])

@router.post("", status_code=status.HTTP_201_CREATED, tags=["Departments"],response_model=DepartmentResponse)
async def create(body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    name = body.name
   
    department=await department_service.create(db,name)
    return department

@router.get("",tags=["Departments"],response_model=list[DepartmentResponse])
async def fetch_all(db:AsyncSession = Depends(get_db)):
    department= await department_service.fetch_all(db)
    return department

@router.get("/{dept_id}",tags=["Departments"],response_model=DepartmentDetailResponse)
async def fetch_one(dept_id:int, db:AsyncSession= Depends(get_db)):
    department=await department_service.fetch_one(dept_id,db)
    return department

@router.put("/{dept_id}",tags=["Departments"],response_model=DepartmentResponse)
async def update(body: DepartmentUpdate,dept_id:int,db:AsyncSession = Depends(get_db)):
    name=body.name
    department= await department_service.update(dept_id,db,name)
    return department

@router.delete("/{dept_id}",tags=["Departments"],response_model=DepartmentResponse)
async def remove(dept_id:int, db:AsyncSession= Depends(get_db)):
    department= await department_service.remove(dept_id,db)
    return department