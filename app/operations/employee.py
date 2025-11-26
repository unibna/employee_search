from sqlmodel import Session, select, func, or_
from sqlalchemy import func as sql_func
from typing import List, Tuple

from app.models.employee import Employee
from app.schemas.employee import ListEmployeeFilters


def get_employees(
    session: Session,
    filters: ListEmployeeFilters
) -> Tuple[int, List[Employee]]:
    base_query = select(Employee)
    count_query = select(func.count(Employee.id))
    
    if filters.positions:
        base_query = base_query.where(Employee.position.in_(filters.positions))
        count_query = count_query.where(Employee.position.in_(filters.positions))

    if filters.locations:
        base_query = base_query.where(Employee.location.in_(filters.locations))
        count_query = count_query.where(Employee.location.in_(filters.locations))

    if filters.company_ids:
        base_query = base_query.where(Employee.company_id.in_(filters.company_ids))
        count_query = count_query.where(Employee.company_id.in_(filters.company_ids))

    if filters.department_ids:
        base_query = base_query.where(Employee.department_id.in_(filters.department_ids))
        count_query = count_query.where(Employee.department_id.in_(filters.department_ids))

    if filters.statuses:
        base_query = base_query.where(Employee.status.in_(filters.statuses))
        count_query = count_query.where(Employee.status.in_(filters.statuses))

    if filters.search:
        search_pattern = f"%{filters.search}%"
        search_condition = or_(
            sql_func.lower(Employee.first_name).like(sql_func.lower(search_pattern)),
            sql_func.lower(Employee.last_name).like(sql_func.lower(search_pattern)),
            sql_func.lower(Employee.email).like(sql_func.lower(search_pattern))
        )
        base_query = base_query.where(search_condition)
        count_query = count_query.where(search_condition)
    
    total = session.exec(count_query).one()

    paginated_query = base_query.offset((filters.page - 1) * filters.page_size).limit(filters.page_size)
    employees = list(session.exec(paginated_query).all())

    return total, employees

