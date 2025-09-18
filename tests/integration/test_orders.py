from fastapi.testclient import TestClient
from fastapi import HTTPException
import pytest
from pytest_mock import mocker
from datetime import datetime

from src.main import app

client = TestClient(app)

def test_create_order_success():
    order_data = {
            "customer_id": 7,
            "price": 12.00,
            "item_id": 1
        }
    response = client.post("/api/v1/orders", json=order_data)

    assert response.status_code == 201
    assert response.json() == {"message": "Order created successfully"}

def test_get_order_success():

    response = client.get("/api/v1/orders/20")

    assert response.status_code == 200

def test_delete_order_success(mocker):
    mock_order_repo = mocker.patch("src.order.service.order_repo")
    mock_order_repo.get_customer_by_id.return_value = None

    response = client.delete("/api/v1/orders/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Order deleted successfully"}

def test_get_non_existing_order():

    response = client.get("/api/v1/orders/1000")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}

def test_delete_non_existing_order():

    response = client.delete("/api/v1/orders/1000")

    assert response.status_code == 204
