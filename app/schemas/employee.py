from pydantic import BaseModel

from app.models.employee import EmployeeStatus


class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str | None = None
    phone_number: str | None = None
    status: EmployeeStatus
    company_name: str | None = None
    department_name: str | None = None
    position: str | None = None
    location: str | None = None


class ListEmployeeFilters(BaseModel):
    page: int = 1
    page_size: int = 10
    status: EmployeeStatus | None = None
    company_id: str | None = None
    department_id: str | None = None
    position: str | None = None
    location: str | None = None
    search: str | None = None

