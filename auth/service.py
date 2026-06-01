from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, decode_access_token, verify_password,create_refresh_token
from employees import employee_repo
from exceptions import UnauthorizedException

async def login(db:AsyncSession,email:str,password:str)->str:
    db_employee= await employee_repo.get_by_email(email,db)
    #print("hello")
    if db_employee is None:
        raise UnauthorizedException("Invalid email or password")

    #print(db_employee.password_hash)
    
    if not verify_password(password, db_employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    
    access_token=create_access_token({"id": db_employee.id, "email": db_employee.email,"role":db_employee.role.value})

    refresh_token=create_refresh_token({"id": db_employee.id,"email":db_employee.email,"role":db_employee.role.value})
    
    return {"access_token": access_token,"refresh_token": refresh_token}
    
async def refresh(refresh_token:str):
    payload=decode_access_token(refresh_token)

    if payload is None:
        raise UnauthorizedException(detail="Invalid refresh token")

    new_access_token= create_access_token({"id":payload["id"],"email": payload["email"]})

    return new_access_token