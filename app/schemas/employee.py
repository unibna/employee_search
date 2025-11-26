from pydantic import BaseModel
from typing import List

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
    statuses: List[EmployeeStatus] = []
    company_ids: List[int] = []
    department_ids: List[int] = []
    positions: List[str] = []
    locations: List[str] = []
    search: str | None = None

