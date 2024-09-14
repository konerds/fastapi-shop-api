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
    response_get_products = client.get("/api/products/")
    assert response_get_products.status_code == 200
    data_get_products = response_get_products.json()
    assert "data" in data_get_products
    assert len(data_get_products["data"]) == 1
    assert "id" in data_get_products["data"][0]
    assert data_get_products["data"][0]["name"] == "product1"
    assert data_get_products["data"][0]["price"] == 100
    assert data_get_products["data"][0]["stock"] == 10


def test_post_product_handler(client):
    product1 = {
        "name": "product1",
        "price": 100,
        "stock": 10
    }
    response_post_products = client.post(
        "/api/products/",
        json=product1
    )
    assert response_post_products.status_code == 200
    data_post_products = response_post_products.json()
    assert "name" in data_post_products
    assert data_post_products["name"] == "product1"
    assert data_post_products["price"] == 100
    assert data_post_products["stock"] == 10
    with SessionLocal() as session:
        from db.repositories import ProductRepository
        product_repository = ProductRepository(session)
        products = product_repository.get_all()
        assert any(
            p.id is not None
            and
            p.name == "product1"
            for p in products
        )
