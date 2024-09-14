from db.models import Member
from tests.conftest import SessionLocal


def test_get_members_handler(client):
    with SessionLocal() as session:
        from db.repositories import MemberRepository
        member_repository = MemberRepository(session)
        member_repository.save(
            Member.create(
                name="member1",
                address="address of member1"
            )
        )
    response = client.get("/api/members")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "member1"


def test_post_member_handler(client):
    member1 = {
        "name": "member1",
        "address": "address of member1"
    }
    response = client.post("/api/members", json=member1)
    assert response.status_code == 200
    created_member = response.json()
    assert created_member["name"] == member1["name"]
    with SessionLocal() as session:
        from db.repositories import MemberRepository
        member_repository = MemberRepository(session)
        members = member_repository.get_all()
        assert any(m.name == "member1" for m in members)
