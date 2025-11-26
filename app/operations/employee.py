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
    
    if filters.position:
        base_query = base_query.where(Employee.position == filters.position)
        count_query = count_query.where(Employee.position == filters.position)

    if filters.location:
        base_query = base_query.where(Employee.location == filters.location)
        count_query = count_query.where(Employee.location == filters.location)

    if filters.company_id:
        base_query = base_query.where(Employee.company_id == filters.company_id)
        count_query = count_query.where(Employee.company_id == filters.company_id)

    if filters.department_id:
        base_query = base_query.where(Employee.department_id == filters.department_id)
        count_query = count_query.where(Employee.department_id == filters.department_id)

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

