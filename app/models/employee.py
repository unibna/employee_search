from enum import Enum
from sqlmodel import Field, SQLModel
from typing import Optional


class EmployeeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TERMINATED = "TERMINATED"


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    phone_number: Optional[str] = None
    status: EmployeeStatus = Field(index=True)
    department_id: Optional[int] = Field(default=None, foreign_key="department.id", index=True)
    company_id: int = Field(foreign_key="company.id", index=True)
    organisation_id: int = Field(foreign_key="organisation.id", index=True)
    position: Optional[str] = Field(index=True)
    location: Optional[str] = Field(index=True)

