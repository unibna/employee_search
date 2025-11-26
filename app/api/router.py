from fastapi import APIRouter

from app.api.v1.employee import router as employee_router

api_router = APIRouter()
api_router.include_router(employee_router, prefix="/employees", tags=["employee"])

