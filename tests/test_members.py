from db.models import Member
from db.repositories import MemberRepository
from tests.conftest import SessionLocal


def test_get_members(client):
    with SessionLocal() as session:
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


def test_post_member(client):
    member1 = {
        "name": "member1",
        "address": "address of member1"
    }
    response = client.post("/api/members", json=member1)
    assert response.status_code == 200
    created_member = response.json()
    assert created_member["name"] == member1["name"]
    with SessionLocal() as session:
        matched_member_in_db = session.query(Member).filter_by(name="member1").first()
        assert matched_member_in_db.id is not None
        assert matched_member_in_db.name == "member1"
        assert matched_member_in_db.address == "address of member1"
