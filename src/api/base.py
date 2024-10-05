from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.repositories import MemberRepository
from dependencies import get_db, templates
from schema.res import DtoResHealth

router = APIRouter()


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
    if member.is_admin:
        return RedirectResponse("/admin/products")
    return RedirectResponse("/orders")


@router.get("/signin")
def get_signin_page_handler(request: Request):
    request.session.pop("member_id", None)
    request.session.pop("member_name", None)
    return templates.TemplateResponse(
        "signin.html",
        {
            "request": request,
            "title_page": "Shop Service - Sign In"
        }
    )


@router.get("/signup")
def get_signup_page_handler(request: Request):
    request.session.pop("member_id", None)
    request.session.pop("member_name", None)
    return templates.TemplateResponse(
        "signup.html",
        {
            "request": request,
            "title_page": "Shop Service - Sign Up"
        }
    )


@router.get("/health")
def check_health_handler(session: Session = Depends(get_db)) -> DtoResHealth:
    session.execute("SELECT 1")
    return DtoResHealth(status="OK")
