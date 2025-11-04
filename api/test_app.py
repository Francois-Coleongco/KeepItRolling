import io
import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, UPLOAD_DIR, OUTPUT_DIR

client = TestClient(app)

def test_login_success():
    with patch("auth.authenticate_user") as mock_auth, \
         patch("auth.create_access_token") as mock_token:

        mock_auth.return_value = {"username": "testuser"}
        mock_token.return_value = "fake-jwt-token"

        response = client.post(
            "/token",
            data={"username": "cool", "password": "dude"}
        )

        assert response.status_code == 200
        assert response.json()["authed"] is True
        assert "access_token" in response.cookies

def test_login_failure():
    with patch("auth.authenticate_user") as mock_auth:
        mock_auth.return_value = None

        response = client.post(
            "/token",
            data={"username": "stinky", "password": "doodoo"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

