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
























# # tests/test_api.py
# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_fetch_feeds():
#     response = client.post("/fetch/", json={
#         "urls": ["https://realpython.com/atom.xml"],
#         "max_items": 2
#     })
#     assert response.status_code == 200
#     assert "message" in response.json()

# def test_dashboard():
#     response = client.get("/dashboard/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_delete_user_feed_data():
#     response = client.delete("/delete/")
#     assert response.status_code == 200
#     assert "message" in response.json()

# def test_new_endpoint():
#     # Add your new test here for the new endpoint
#     response = client.post("/new-endpoint/", json={"key": "value"})
#     assert response.status_code == 200
#     assert "message" in response.json()






# 







