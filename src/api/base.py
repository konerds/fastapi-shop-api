from fastapi import APIRouter

from schema.res import DtoResHealth

router = APIRouter()


@router.get("/")
def check_health() -> DtoResHealth:
    return DtoResHealth(status="OK")
