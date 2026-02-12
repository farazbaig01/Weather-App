from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather_endpoint():
    response = client.get("/weather/London")
    # If this fails, the error message below will show up in your logs
    error_msg = f"API returned {response.status_code}. Response body: {response.text}"
    assert response.status_code == 200, error_msg