from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.models import Member
from db.repositories import MemberRepository
from db.session import get_db
from schema.req import DtoReqPostMember
from schema.res import DtoResMembers, DtoResMember

router = APIRouter(prefix="/api/members")


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
    response_model=DtoResMember
)
def post_member_handler(
        req: DtoReqPostMember,
        session: Session = Depends(get_db),
):
    member_repository = MemberRepository(session)
    return DtoResMember.model_validate(
        member_repository.save(
            Member.create(
                req.name,
                req.address
            )
        )
    )
