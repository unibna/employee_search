import json
import random
from pathlib import Path
from sqlmodel import Session, select, func
from typing import Dict, List
from faker import Faker

from app.core.database import engine, init_db
from app.core.config import settings
from app.models.organisation import Organisation
from app.models.company import Company
from app.models.department import Department
from app.models.employee import Employee, EmployeeStatus
from app.models.organisation_settings import OrganisationSettings


fake = Faker()

DATA_DIR = Path(__file__).parent / "__data__"

POSITIONS = [
    "Software Engineer", "Senior Software Engineer", "Lead Software Engineer",
    "Principal Software Engineer", "Software Architect", "DevOps Engineer",
    "QA Engineer", "QA Manager", "Product Manager", "Senior Product Manager",
    "Product Owner", "Scrum Master", "Project Manager", "Program Manager",
    "Business Analyst", "Data Analyst", "Data Scientist", "Data Engineer",
    "Machine Learning Engineer", "UI/UX Designer", "Graphic Designer",
    "Marketing Manager", "Marketing Specialist", "Sales Representative",
    "Sales Manager", "Account Executive", "Customer Success Manager",
    "HR Manager", "HR Specialist", "Recruiter", "Finance Manager",
    "Financial Analyst", "Accountant", "Controller", "CFO",
    "Operations Manager", "Operations Analyst", "Supply Chain Manager",
    "Logistics Coordinator", "IT Manager", "IT Support Specialist",
    "Network Administrator", "Security Engineer", "Legal Counsel",
    "Compliance Officer", "Executive Assistant", "Office Manager",
    "Facilities Manager", "Research Scientist", "Clinical Research Coordinator"
]

LOCATIONS = [
    "Singapore", "Kuala Lumpur", "Jakarta", "Bangkok", "Manila",
    "Ho Chi Minh City", "Hanoi", "Phnom Penh", "Yangon", "Vientiane",
    "Hong Kong", "Taipei", "Seoul", "Tokyo", "Shanghai",
    "Beijing", "Sydney", "Melbourne", "Auckland", "Wellington"
]


def load_json_data(filename: str) -> List[Dict]:
    file_path = DATA_DIR / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_organisations(session: Session) -> Dict[str, Organisation]:
    print("Creating organisations...")
    organisations_data = load_json_data("organisation_data.json")
    org_map = {}
    
    for org_data in organisations_data:
        existing = session.exec(
            select(Organisation).where(Organisation.name == org_data["name"])
        ).first()
        
        if existing:
            org_map[org_data["name"]] = existing
            print(f"  Organisation '{org_data['name']}' already exists")
        else:
            organisation = Organisation(name=org_data["name"])
            session.add(organisation)
            session.commit()
            session.refresh(organisation)
            org_map[org_data["name"]] = organisation
            print(f"  Created organisation: {organisation.name} (ID: {organisation.id})")
    
    return org_map


def create_companies(session: Session, org_map: Dict[str, Organisation]) -> Dict[str, Company]:
    print("\nCreating companies...")
    companies_data = load_json_data("company_data.json")
    company_map = {}
    
    for company_data in companies_data:
        org_name = company_data["organisation_name"]
        organisation = org_map.get(org_name)
        
        if not organisation:
            print(f"  Warning: Organisation '{org_name}' not found for company '{company_data['name']}'")
            continue
        
        existing = session.exec(
            select(Company).where(
                Company.name == company_data["name"],
                Company.organisation_id == organisation.id
            )
        ).first()
        
        if existing:
            company_map[company_data["name"]] = existing
            print(f"  Company '{company_data['name']}' already exists")
        else:
            company = Company(
                name=company_data["name"],
                organisation_id=organisation.id
            )
            session.add(company)
            session.commit()
            session.refresh(company)
            company_map[company_data["name"]] = company
            print(f"  Created company: {company.name} (ID: {company.id})")
    
    return company_map


def create_departments(session: Session, org_map: Dict[str, Organisation], company_map: Dict[str, Company]) -> List[Department]:
    print("\nCreating departments...")
    departments_data = load_json_data("department_data.json")
    departments = []
    
    for dept_data in departments_data:
        org_name = dept_data["organisation_name"]
        company_name = dept_data["company_name"]
        
        organisation = org_map.get(org_name)
        company = company_map.get(company_name)
        
        if not organisation:
            print(f"  Warning: Organisation '{org_name}' not found for department '{dept_data['name']}'")
            continue
        if not company:
            print(f"  Warning: Company '{company_name}' not found for department '{dept_data['name']}'")
            continue
        
        existing = session.exec(
            select(Department).where(
                Department.name == dept_data["name"],
                Department.company_id == company.id,
                Department.organisation_id == organisation.id
            )
        ).first()
        
        if existing:
            departments.append(existing)
            print(f"  Department '{dept_data['name']}' already exists")
        else:
            department = Department(
                name=dept_data["name"],
                company_id=company.id,
                organisation_id=organisation.id
            )
            session.add(department)
            session.commit()
            session.refresh(department)
            departments.append(department)
            print(f"  Created department: {department.name} (ID: {department.id})")
    
    return departments


def create_organisation_settings(session: Session, org_map: Dict[str, Organisation]) -> None:
    print("\nCreating organisation settings...")
    settings_data = load_json_data("organisation_settings_data.json")
    
    for setting_data in settings_data:
        org_name = setting_data["organisation_name"]
        organisation = org_map.get(org_name)
        
        if not organisation:
            print(f"  Warning: Organisation '{org_name}' not found for settings")
            continue
        
        existing = session.exec(
            select(OrganisationSettings).where(
                OrganisationSettings.organisation_id == organisation.id
            )
        ).first()
        
        if existing:
            print(f"  Settings for organisation '{org_name}' already exist")
        else:
            org_settings = OrganisationSettings(
                organisation_id=organisation.id,
                settings=setting_data["settings"]
            )
            session.add(org_settings)
            session.commit()
            print(f"  Created settings for organisation: {org_name}")


def create_employees(session: Session, num_employees: int = 5_000_000) -> None:
    print(f"\nCreating up to {num_employees:,} employees...")
    
    # Count existing employees first
    existing_count = session.exec(select(func.count(Employee.id))).one()
    print(f"  Found {existing_count:,} existing employees")
    
    if existing_count >= num_employees:
        print(f"  ✓ Already have {existing_count:,} employees (target: {num_employees:,})")
        return
    
    employees_needed = num_employees - existing_count
    print(f"  Need to create {employees_needed:,} more employees")
    
    companies = list(session.exec(select(Company)).all())
    departments = list(session.exec(select(Department)).all())
    
    if not companies:
        print("  Error: No companies found. Please create companies first.")
        return
    
    if not departments:
        print("  Warning: No departments found. Employees will be created without departments.")
    
    # Get the highest email counter from existing employees
    # Extract number from email pattern "employee{number}@test.com"
    max_email_num = 0
    if existing_count > 0:
        # Get a sample of existing emails to find the max counter
        # We'll use a query to find the max ID and estimate, or parse emails
        # For simplicity, we'll start from existing_count + 1
        max_email_num = existing_count
    
    # Use smaller batch size for SQLite to avoid locking issues
    batch_size = 5000 if settings.database_url.startswith("sqlite") else 10000
    total_batches = (employees_needed + batch_size - 1) // batch_size
    
    email_counter = max_email_num
    total_created = 0
    
    for batch_num in range(total_batches):
        employees_data = []
        batch_start = batch_num * batch_size
        batch_end = min(batch_start + batch_size, employees_needed)
        batch_count = batch_end - batch_start
        
        for i in range(batch_count):
            company = random.choice(companies)
            department = random.choice(departments) if departments else None
            
            if department:
                if department.organisation_id != company.organisation_id or department.company_id != company.id:
                    department = None
            
            first_name = fake.first_name()
            last_name = fake.last_name()
            email_counter += 1
            email = f"employee{email_counter}@test.com"
            
            # Create as dictionary for bulk insert
            employee_dict = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": fake.phone_number() if random.random() > 0.1 else None,
                "status": random.choice(list(EmployeeStatus)).value,  # Use .value for enum
                "department_id": department.id if department else None,
                "company_id": company.id,
                "organisation_id": company.organisation_id,
                "position": random.choice(POSITIONS),
                "location": random.choice(LOCATIONS)
            }
            employees_data.append(employee_dict)
        
        # Use bulk_insert_mappings for better performance and compatibility
        session.bulk_insert_mappings(Employee, employees_data)
        session.commit()
        session.expunge_all()  # Clear session to free memory
        
        total_created += len(employees_data)
        current_total = existing_count + total_created
        progress_pct = (total_created / employees_needed * 100) if employees_needed > 0 else 100
        print(f"  Progress: {total_created:,} / {employees_needed:,} new employees created ({progress_pct:.1f}%) | Total: {current_total:,} / {num_employees:,}")
    
    final_count = session.exec(select(func.count(Employee.id))).one()
    print(f"  ✓ Successfully created employees. Total count: {final_count:,} / {num_employees:,}")


def setup_all_data(num_employees: int = 5_000_000) -> None:
    print("=" * 60)
    print("Setting up test data...")
    print("=" * 60)
    
    init_db()
    
    with Session(engine) as session:
        # org_map = create_organisations(session)
        
        # company_map = create_companies(session, org_map)

        # departments = create_departments(session, org_map, company_map)
        
        # create_organisation_settings(session, org_map)
        
        create_employees(session, num_employees)
    
    print("\n" + "=" * 60)
    print("Test data setup completed!")
    print("=" * 60)


if __name__ == "__main__":
    setup_all_data()

