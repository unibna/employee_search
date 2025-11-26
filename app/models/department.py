from sqlmodel import Field, SQLModel
from typing import Optional


class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    company_id: int = Field(foreign_key="company.id", index=True)
    organisation_id: int = Field(foreign_key="organisation.id", index=True)

