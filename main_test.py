import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_weather_endpoint():
    response = client.get("/weather/London")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert isinstance(data["temperature"], float)
    