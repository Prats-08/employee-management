from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    department: str
    salary: float = Field(gt=0)


class Employee(EmployeeCreate):
    id: int

class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    department: str | None = None
    salary: float | None = Field(default=None, gt=0)