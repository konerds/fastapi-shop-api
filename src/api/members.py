from fastapi import status, Request, APIRouter, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.models import Member
from db.repositories import MemberRepository
from dependencies import get_db, encrypt, verify, TEMPLATE_DIR
from schema.req import DtoReqPostMember, DtoReqSigninMember
from schema.res import DtoResMembers, DtoResMember

router = APIRouter(prefix="/api/members")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get(
    "/",
    response_model=DtoResMembers
)
def get_members_handler(
        sort_type: str = Query(
            "asc",
            alias="sort_type"
        ),
        session: Session = Depends(get_db)
):
    member_repository = MemberRepository(session)
    members = member_repository.get_all(
        sort_type == "desc"
    )
    return DtoResMembers(
        data=[
            DtoResMember.model_validate(member)
            for member in members
        ]
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def post_member_handler(
        req_body: DtoReqPostMember,
        session: Session = Depends(get_db)
):
    member_repository = MemberRepository(session)
    member = member_repository.get_one_by_email(req_body.email)
    if member is not None:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 이메일입니다..."
        )
    member = member_repository.save(
        Member.create(
            False,
            req_body.email,
            encrypt(req_body.password),
            req_body.name
        )
    )
    DtoResMember.model_validate(member)
    return {
        "message": "회원가입에 성공하였습니다!",
        "data": member
    }


@router.post(
    "/signin",
    status_code=status.HTTP_201_CREATED
)
def signin_handler(
        request: Request,
        req_body: DtoReqSigninMember,
        session: Session = Depends(get_db)
):
    member_repository = MemberRepository(session)
    member = member_repository.get_one_by_email(req_body.email)
    if member and verify(req_body.password, member.password):
        request.session["member_id"] = member.id
        return {
            "message": "로그인에 성공하였습니다!"
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="로그인에 실패하였습니다..."
        )


@router.post(
    "/signout"
)
def signout_handler(
        request: Request
):
    request.session.pop("member_id", None)
    return {
        "message": "로그아웃에 성공하였습니다!"
    }
