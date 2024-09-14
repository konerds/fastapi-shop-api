from fastapi import APIRouter

from schema.res import DtoResHealth

router = APIRouter()


@router.get("/")
def check_health_handler() -> DtoResHealth:
    return DtoResHealth(status="OK")
