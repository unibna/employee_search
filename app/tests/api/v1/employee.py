import os
import tempfile

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlmodel import Session, create_engine, SQLModel

from app.api.deps.rate_limit_deps import rate_limit_dependency
from app.core.database import get_session
from app.main import app
from app.models import Company, Department, Employee, Organisation
from app.models.employee import EmployeeStatus


@pytest.fixture(scope="function")
def test_db():
    # Use a temporary file for the database to avoid connection issues
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    engine = create_engine(f"sqlite:///{db_path}", echo=False, connect_args={"check_same_thread": False})
    
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()
    
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture(scope="function")
def session(test_db):
    with Session(test_db) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def test_data(session):
    org = Organisation(name="Test Organisation")
    session.add(org)
    session.commit()
    session.refresh(org)
    
    company1 = Company(name="Company A", organisation_id=org.id)
    company2 = Company(name="Company B", organisation_id=org.id)
    session.add_all([company1, company2])
    session.commit()
    session.refresh(company1)
    session.refresh(company2)
    
    dept1 = Department(name="Engineering", company_id=company1.id, organisation_id=org.id)
    dept2 = Department(name="Sales", company_id=company2.id, organisation_id=org.id)
    session.add_all([dept1, dept2])
    session.commit()
    session.refresh(dept1)
    session.refresh(dept2)
    
    employees = [
        Employee(
            first_name="John", last_name="Doe", email="john.doe@test.com",
            status=EmployeeStatus.ACTIVE, company_id=company1.id,
            organisation_id=org.id, department_id=dept1.id,
            position="Software Engineer", location="Singapore"
        ),
        Employee(
            first_name="Jane", last_name="Smith", email="jane.smith@test.com",
            status=EmployeeStatus.ACTIVE, company_id=company1.id,
            organisation_id=org.id, department_id=dept1.id,
            position="Senior Engineer", location="Kuala Lumpur"
        ),
        Employee(
            first_name="Bob", last_name="Johnson", email="bob.johnson@test.com",
            status=EmployeeStatus.INACTIVE, company_id=company2.id,
            organisation_id=org.id, department_id=dept2.id,
            position="Sales Rep", location="Singapore"
        ),
    ]
    session.add_all(employees)
    session.commit()
    
    return {
        "org": org,
        "companies": [company1, company2],
        "departments": [dept1, dept2],
        "employees": employees
    }


@pytest.fixture(scope="function")
def client(test_db, test_data):
    SQLModel.metadata.create_all(test_db)
    
    def override_get_session():
        with Session(test_db) as session:
            yield session
    
    app.dependency_overrides[get_session] = override_get_session

    async def override_rate_limit(request: Request):
        return True
    app.dependency_overrides[rate_limit_dependency] = override_rate_limit
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()


class TestListEmployeesEndpoint:
    def test_list_employees_success(self, client, test_data):
        response = client.get("/api/v1/employees")
        
        assert response.status_code == 200
        data = response.json()
        assert "page" in data
        assert "page_size" in data
        assert "total" in data
        assert "total_pages" in data
        assert "data" in data
        assert len(data["data"]) == 3

    def test_combined_filters(self, client, test_data):
        company_id = test_data["companies"][0].id
        company_name = test_data["companies"][0].name
        response = client.get(
            "/api/v1/employees"
            "?statuses[]=ACTIVE"
            f"&company_ids[]={company_id}"
            "&locations[]=Singapore"
        )
        data = response.json()
        
        assert data["total"] == 1
        emp = data["data"][0]
        assert emp["status"] == "ACTIVE"
        assert emp["company_name"] == company_name
        assert emp["location"] == "Singapore"
    
    def test_empty_result(self, client, test_data):
        response = client.get("/api/v1/employees?statuses[]=TERMINATED")
        data = response.json()
        
        assert data["total"] == 0
        assert len(data["data"]) == 0
        assert data["total_pages"] == 0
    
    def test_response_structure(self, client, test_data):
        response = client.get("/api/v1/employees")
        data = response.json()
        
        assert isinstance(data["page"], int)
        assert isinstance(data["page_size"], int)
        assert isinstance(data["total"], int)
        assert isinstance(data["total_pages"], int)
        assert isinstance(data["data"], list)
        
        if data["data"]:
            emp = data["data"][0]
            assert "id" in emp
            assert "first_name" in emp
            assert "last_name" in emp
            assert "email" in emp
            assert "status" in emp
    
    def test_invalid_query_parameters(self, client, test_data):
        response = client.get("/api/v1/employees?page=0&page_size=0&page_size=101")
        assert response.status_code == 422
