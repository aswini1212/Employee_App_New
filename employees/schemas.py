from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field,field_validator, model_validator

from models.employee import EmployeeRole


#-----schemas for adress table-----
class AddressCreate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v:str)->str:
        if not v.isdigit():
            raise ValueError("Postalcode must contain only digits(0-9)")
        return v
    
    @model_validator(mode="after")

    def postal_code_length_for_country(self):

        country = self.country.strip().upper()

        n = len(self.postal_code)

        if country in ("US", "USA") and n != 5:

            raise ValueError("US ZIP codes must be exactly 5 digits")

        elif country == "IN" and n != 6:

            raise ValueError("Indian PIN codes must be exactly 6 digits")

        return self

class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    line1: str
    city: str
    postal_code: str
    country: str

class AddressUpdate(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError(
                "Postal code must contain only digits (0-9)"
            )
        return v

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        country = self.country.strip().upper()
        n = len(self.postal_code)

        if country in ("US", "USA") and n != 5:
            raise ValueError(
                "US ZIP codes must be exactly 5 digits"
            )

        elif country == "IN" and n != 6:
            raise ValueError(
                "Indian PIN codes must be exactly 6 digits"
            )

        return self
    

#----schemas for employee table-----
class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: str
    age: int | None = Field(ge=0,le=150)
    password: str = Field(min_length=6)
    role: EmployeeRole
    addresses: list[AddressCreate] | None = None

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    id: int
    name:str
    email: str
    age:int | None

    addresses: list[AddressResponse] = []

class EmployeeResponseId(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    id:int
    name:str
    email:str
    age:int | None
    created_at: datetime
    updated_at: datetime
    
class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1)
    email: str
    age: int | None = Field(ge=0,le=150)
    password: str = Field(min_length=6)
    addresses: list[AddressCreate ]=[]

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int | None) -> int | None:
        if v is None:
            return v
        if v < 0:
            raise ValueError("age is negative")
        if v >100:
            print("age is greater than 100")
        return v
    
#----schemas for emp_dep_assoc table----
class AssociationResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    department_id:int
    employee_id:int