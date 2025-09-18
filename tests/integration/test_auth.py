from fastapi.testclient import TestClient
import pytest
from pytest_mock import mocker

from src.main import app

client = TestClient(app)

def test_register_success(mocker):
    # Mock the global customer_repo instance
    mock_customer_repo = mocker.patch("src.customer.service.customer_repo")

    mock_customer_repo.create_customer.return_value = None

    register_data = {
        "name": "name",
        "email": "john.doe@example.com",
        "password": "password",
        "phone_number": "254700000000"
    }
    response = client.post("/api/v1/register", json=register_data)

    assert response.status_code == 201
    assert response.json() == "Customer registered successfully"

def test_register_with_invalid_email():
    login_data = {
        "name": "name",
        "email": "invalid_email",
        "password": "password",
        "phone_number": "254700000000"
    }
    response = client.post("/api/v1/register", json=login_data)

    # Raise ValidationError because of invalid email fomart
    assert response.status_code == 422

def test_register_with_duplicate_email():
    register_data = {
        "name": "name",
        "email": "john.doe@example.com", # Ensure this email already exists in the database
        "password": "password",
        "phone_number": "245700000000"
    }
    response = client.post("/api/v1/register", json=register_data)

    assert response.status_code == 409
    assert response.json() == {"detail": "User with the same email already exists"}

def test_login_success():
    login_data = {
        "email": "john.doe@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/login", json=login_data)

    assert response.status_code == 200

def test_login_with_invalid_email():
    login_data = {
        "email": "invalid@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/login", json=login_data)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid login credentials"}
