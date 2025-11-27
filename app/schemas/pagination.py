from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar
from typing_extensions import List

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    page: int
    page_size: int
    total: int
    total_pages: int
    data: List[T]

