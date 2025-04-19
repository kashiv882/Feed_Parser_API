from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

def test_secure_api_with_mock_token():
    with patch("auth0.authentication.GetToken") as mock_auth:
        mock_auth.return_value = {"access_token": "fake_token"}
        response = client.get(
            "/dashboard",
            headers={"Authorization": "Bearer fake_token"}
        )
        assert response.status_code == 200