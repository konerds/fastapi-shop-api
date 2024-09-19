from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.repositories import MemberRepository
from dependencies import get_db
from schema.res import DtoResHealth

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_root_page_handler(
        request: Request,
        session: Session = Depends(get_db)
):
    member_id = request.session.get("member_id")
    if member_id is None:
        return RedirectResponse("/signin")
    member_repository = MemberRepository(session)
    member = member_repository.get_one(member_id)
    if member is None:
        return RedirectResponse("/signin")
    if member.is_admin is True:
        return RedirectResponse("/admin/products")
    return RedirectResponse("/orders")


@router.get("/signin")
def get_signin_page_handler(request: Request):
    member_id = request.session.get("member_id")
    if member_id is not None:
        return RedirectResponse("/")
    return templates.TemplateResponse(
        "signin.html",
        {
            "title_page": "Shop Service - Sign In",
            "request": request
        }
    )


@router.get("/signup")
def get_signup_page_handler(request: Request):
    member_id = request.session.get("member_id")
    if member_id is not None:
        return RedirectResponse("/")
    return templates.TemplateResponse(
        "signup.html",
        {
            "title_page": "Shop Service - Sign Up",
            "request": request
        }
    )


@router.get("/health")
def check_health_handler() -> DtoResHealth:
    return DtoResHealth(status="OK")
