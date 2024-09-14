def test_post_order_handler(client):
    member1 = {
        "name": "member1",
        "address": "address of member1"
    }
    response_members = client.post("/api/members/", json=member1)
    assert response_members.status_code == 200
    data_members = response_members.json()
    product1 = {
        "name": "product1",
        "price": 100,
        "stock": 10
    }
    response_products = client.post("/api/products/", json=product1)
    assert response_products.status_code == 200
    data_products = response_products.json()
    order1 = {
        "member_id": data_members["id"],
        "product_id": data_products["id"],
        "quantity": 5
    }
    response_orders = client.post("/api/orders/", json=order1)
    assert response_orders.status_code == 200
    data_orders = response_orders.json()
    assert "id" in data_orders
    assert data_orders["member_id"] == data_members["id"]
    assert data_orders["products"][0]["id"] == data_products["id"]
    assert data_orders["products"][0]["name"] == "product1"
    assert data_orders["products"][0]["price"] == 100
    assert data_orders["products"][0]["quantity"] == 5
