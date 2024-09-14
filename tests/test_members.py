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
    response_get_members = client.get("/api/members")
    assert response_get_members.status_code == 200
    data_get_members = response_get_members.json()
    assert len(data_get_members["data"]) == 1
    assert "id" in data_get_members["data"][0]
    assert data_get_members["data"][0]["name"] == "member1"
    assert data_get_members["data"][0]["address"] == "address of member1"


def test_post_member_handler(client):
    member1 = {
        "name": "member1",
        "address": "address of member1"
    }
    response_post_members = client.post("/api/members", json=member1)
    assert response_post_members.status_code == 200
    data_post_members = response_post_members.json()
    assert data_post_members["name"] == member1["name"]
    assert data_post_members["address"] == member1["address"]
    with SessionLocal() as session:
        from db.repositories import MemberRepository
        member_repository = MemberRepository(session)
        members = member_repository.get_all()
        assert any(
            m.id is not None
            and
            m.name == "member1"
            and
            m.address == "address of member1"
            for m in members
        )
