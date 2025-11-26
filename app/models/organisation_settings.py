from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional, Dict, Any


class OrganisationSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id", index=True)
    settings: Dict[str, Any] = Field(sa_column=Column(JSON))

