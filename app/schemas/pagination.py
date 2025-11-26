from pydantic import BaseModel
from typing import Generic, TypeVar
from typing_extensions import List

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    page_size: int
    total: int
    total_pages: int
    data: List[T]
    
    class Config:
        arbitrary_types_allowed = True

