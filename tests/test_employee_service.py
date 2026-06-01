import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from database import Base
from employees import employee_service as employee_service
from employees.schemas import EmployeeCreate

#test using sqlite
@pytest.mark.asyncio
async def test_create_employee_persists_the_record():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as db:
        body = EmployeeCreate(
            name="Ada",
            email="ada@example.com",
            age=54,
            password="secret123",
            addresses=None
        )
        employee = await employee_service.create(db, body.name,body.email,body.age,body.password,body.addresses)
        

        assert employee.id is not None
        assert employee.name == "Ada"
        assert employee.email == "ada@example.com"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()