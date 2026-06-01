from pydantic import BaseModel, ConfigDict, Field, field_validator


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=1)


class DepartmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def name_must_not_contain_numbers(cls, v: str) -> str:
        if any(ch.isdigit() for ch in v):
            raise ValueError("name must not contain digits")
        return v


class DepartmentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)


class EmployeeBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age: int | None


class DepartmentDetailResponse(DepartmentResponse):
    employees: list[EmployeeBrief] = []
