from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from schema.res import DtoResHealth

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_root_page_handler(request: Request):
    member_id = request.session.get("member_id")
    if member_id is None:
        return RedirectResponse("/signin")
    return RedirectResponse("/orders")


@router.get("/signin")
def get_signin_page_handler(request: Request):
    return templates.TemplateResponse(
        "signin.html",
        {
            "request": request
        }
    )


@router.get("/signup")
def get_signup_page_handler(request: Request):
    return templates.TemplateResponse(
        "signup.html",
        {
            "request": request
        }
    )


@router.get("/health")
def check_health_handler() -> DtoResHealth:
    return DtoResHealth(status="OK")
