from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.employee import Employee, ListEmployeeFilters
from app.schemas.pagination import PaginatedResponse
from app.operations.employee import get_employees

router = APIRouter()


def get_total_pages(total: int, page_size: int) -> int:
    return (total + page_size - 1) // page_size


@router.get("", response_model=PaginatedResponse[Employee])
def list_employees(
    query_params: ListEmployeeFilters = Depends(),
    session: Session = Depends(get_session),
):
    total, employees = get_employees(session=session, filters=query_params)

    return {
        "page": query_params.page,
        "page_size": query_params.page_size,
        "total": total,
        "total_pages": get_total_pages(total, query_params.page_size),
        "data": employees,
    }
