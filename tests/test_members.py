from db.models import Member
from dependencies import verify
from tests.conftest import SessionLocal


def test_get_members_handler(client):
    with SessionLocal() as session:
        from db.repositories import MemberRepository
        member_repository = MemberRepository(session)
        member_repository.save(
            Member.create(
                is_admin=False,
                email="member1@konerds.buzz",
                password="aaaaa11111",
                name="member1"
            )
        )
        member_repository.save(
            Member.create(
                is_admin=False,
                email="member2@konerds.buzz",
                password="aaaaa11111",
                name="member2"
            )
        )
        member_repository.save(
            Member.create(
                is_admin=False,
                email="member3@konerds.buzz",
                password="aaaaa11111",
                name="member3"
            )
        )
    response_get_members = client.get("/api/members")
    assert response_get_members.status_code == 200
    data_get_members = response_get_members.json()
    members = data_get_members["data"]
    assert len(members) == 3
    assert "id" in members[0]
    assert members[0]["name"] == "member1"
    assert "id" in members[1]
    assert members[1]["name"] == "member2"
    assert "id" in members[2]
    assert members[2]["name"] == "member3"


def test_post_member_handler(client):
    member1 = {
        "email": "member1@konerds.buzz",
        "password": "aaaaa11111",
        "name": "member1"
    }
    response_post_members = client.post("/api/members", json=member1)
    assert response_post_members.status_code == 201
    data_post_members = response_post_members.json()
    assert data_post_members["message"] == "회원가입에 성공하였습니다!"
    saved_member = data_post_members["data"]
    assert saved_member["email"] == member1["email"]
    assert verify(member1["password"], saved_member["password"])
    assert saved_member["name"] == member1["name"]
    with SessionLocal() as session:
        from db.repositories import MemberRepository
        member_repository = MemberRepository(session)
        members = member_repository.get_all()
        assert any(
            m.id is not None
            and
            m.email == "member1@konerds.buzz"
            and
            m.name == "member1"
            for m in members
        )
