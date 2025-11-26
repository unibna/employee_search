from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.schemas.employee import Employee, ListEmployeeFilters
from app.schemas.pagination import PaginatedResponse
from app.operations.employee import get_employees
from app.models.employee import EmployeeStatus

router = APIRouter()


def get_total_pages(total: int, page_size: int) -> int:
    return (total + page_size - 1) // page_size


@router.get("", response_model=PaginatedResponse[Employee])
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    statuses: List[EmployeeStatus] = Query(default=[], alias="statuses[]"),
    company_id: str | None = Query(None),
    department_id: str | None = Query(None),
    position: str | None = Query(None),
    location: str | None = Query(None),
    search: str | None = Query(None),
    session: Session = Depends(get_session),
):
    filters = ListEmployeeFilters(
        page=page,
        page_size=page_size,
        statuses=statuses,
        company_id=company_id,
        department_id=department_id,
        position=position,
        location=location,
        search=search,
    )
    
    total, employees = get_employees(session=session, filters=filters)

    return {
        "page": filters.page,
        "page_size": filters.page_size,
        "total": total,
        "total_pages": get_total_pages(total, filters.page_size),
        "data": employees,
    }

