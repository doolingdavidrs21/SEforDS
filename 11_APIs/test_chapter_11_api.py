"""Tests for Chapter 11 FastAPI endpoints."""

from fastapi.testclient import TestClient
from chapter_11_api import app

client = TestClient(app)


def test_say_hi():
    """Test the /say_hi/ GET endpoint."""
    response = client.get("/say_hi/")
    assert response.status_code == 200
    assert response.json() == {"Hi": "There"}


def test_say_hello():
    """Test the /say_hello/{name} GET endpoint."""
    response = client.get("/say_hello/Alice")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Alice"}


def test_say_hello_with_special_characters():
    """Test the /say_hello/{name} endpoint with special characters."""
    response = client.get("/say_hello/Jean-Pierre")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Jean-Pierre"}


def test_calculate_trendline():
    """Test the /fit_trendline/ POST endpoint with valid data."""
    payload = {
        "timestamps": [2000, 2001, 2002, 2003, 2004],
        "data": [10.0, 12.0, 14.0, 16.0, 18.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "slope" in result
    assert "r_squared" in result
    assert result["slope"] == 2.0  # Perfect linear trend
    assert result["r_squared"] == 1.0  # Perfect fit


def test_calculate_trendline_with_noisy_data():
    """Test the /fit_trendline/ POST endpoint with noisy data."""
    payload = {
        "timestamps": [2000, 2001, 2002, 2003, 2004],
        "data": [10.0, 11.5, 14.5, 15.0, 18.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "slope" in result
    assert "r_squared" in result
    assert isinstance(result["slope"], float)
    assert isinstance(result["r_squared"], float)
    assert 0 <= result["r_squared"] <= 1


def test_calculate_trendline_invalid_input():
    """Test the /fit_trendline/ POST endpoint with invalid data types."""
    payload = {
        "timestamps": ["invalid", "data"],
        "data": [10.0, 12.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_calculate_trendline_missing_field():
    """Test the /fit_trendline/ POST endpoint with missing required field."""
    payload = {
        "timestamps": [2000, 2001, 2002]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_calculate_country_trendline():
    """Test the /country_trendline/{country} GET endpoint."""
    response = client.get("/country_trendline/Australia")
    assert response.status_code == 200
    result = response.json()
    assert "slope" in result
    assert "r_squared" in result
    assert isinstance(result["slope"], float)
    assert isinstance(result["r_squared"], float)


def test_calculate_country_trendline_different_countries():
    """Test the /country_trendline/{country} endpoint with multiple countries."""
    countries = ["Australia", "Canada", "Germany"]
    for country in countries:
        response = client.get(f"/country_trendline/{country}")
        assert response.status_code == 200
        result = response.json()
        assert "slope" in result
        assert "r_squared" in result
