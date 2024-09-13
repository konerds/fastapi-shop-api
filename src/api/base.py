from fastapi import APIRouter

from schemas.res import DtoResHealth

router = APIRouter()


@router.get("/")
def check_health() -> DtoResHealth:
    return DtoResHealth(status="OK")
