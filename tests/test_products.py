from db.models import Product
from tests.conftest import SessionLocal


def test_get_products_handler(client):
    with SessionLocal() as session:
        from db.repositories import ProductRepository
        product_repository = ProductRepository(session)
        product_repository.save(
            Product.create(
                name="product1",
                price=100,
                stock=10
            )
        )
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert data["data"][0]["name"] == "product1"


def test_post_product_handler(client):
    product1 = {
        "name": "product1",
        "price": 100,
        "stock": 10
    }
    response = client.post(
        "/api/products/",
        json=product1
    )
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert data["name"] == "product1"
    assert data["price"] == 100
    assert data["stock"] == 10
    with SessionLocal() as session:
        from db.repositories import ProductRepository
        product_repository = ProductRepository(session)
        products = product_repository.get_all()
        assert any(p.name == "product1" for p in products)
