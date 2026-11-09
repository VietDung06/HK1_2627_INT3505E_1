# def test_product_get(client):
#     # Soft test, only check for successful status code and not content.
#     response = client.get("/products")
#     assert response.status_code == 200

def test_product_get(client, mocker):
    # Soft test, only check for successful status code and not content.
    mocker.patch(
        "api.products.list_products",
        return_value=[{
            "id": 1,
            "sku": "book/lea",
            "name": "Leather Notebook",
            "description": "Placeholder text.",
            "price_cents": 100,
            "qty_in_stock": 100,
            "archived": False
        }]
    )
    response = client.get("/products")
    assert response.status_code == 200