def test_check_health(c):
    r = c.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "OK"}