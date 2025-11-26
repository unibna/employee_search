from sqlmodel import Field, SQLModel
from typing import Optional


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    organisation_id: int = Field(foreign_key="organisation.id", index=True)

