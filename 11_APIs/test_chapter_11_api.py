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


# Edge Case Tests


def test_calculate_trendline_empty_arrays():
    """Test the /fit_trendline/ POST endpoint with empty arrays."""
    payload = {
        "timestamps": [],
        "data": []
    }
    # Empty arrays cause scipy to raise ValueError
    # FastAPI catches this and returns 500
    try:
        response = client.post("/fit_trendline/", json=payload)
        assert response.status_code == 500
    except ValueError:
        # If exception propagates, that's also acceptable for this edge case
        pass


def test_calculate_trendline_single_point():
    """Test the /fit_trendline/ POST endpoint with single data point."""
    payload = {
        "timestamps": [2000],
        "data": [10.0]
    }
    # Single point causes NaN which can't be JSON serialized
    # This should result in 500 error
    try:
        response = client.post("/fit_trendline/", json=payload)
        assert response.status_code == 500
    except ValueError:
        # If NaN serialization fails with exception, that's expected
        pass


def test_calculate_trendline_two_points():
    """Test the /fit_trendline/ POST endpoint with minimum valid data (2 points)."""
    payload = {
        "timestamps": [2000, 2001],
        "data": [10.0, 12.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["slope"] == 2.0
    assert result["r_squared"] == 1.0  # Perfect fit with 2 points


def test_calculate_trendline_mismatched_lengths():
    """Test the /fit_trendline/ POST endpoint with mismatched array lengths."""
    payload = {
        "timestamps": [2000, 2001, 2002],
        "data": [10.0, 12.0]  # One fewer data point
    }
    # Scipy raises ValueError for mismatched lengths
    try:
        response = client.post("/fit_trendline/", json=payload)
        assert response.status_code == 500
    except ValueError:
        # If exception propagates, that's expected for invalid input
        pass


def test_calculate_trendline_negative_values():
    """Test the /fit_trendline/ POST endpoint with negative values."""
    payload = {
        "timestamps": [2000, 2001, 2002, 2003],
        "data": [-10.0, -8.0, -6.0, -4.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["slope"] == 2.0  # Should still calculate correctly
    assert result["r_squared"] == 1.0


def test_calculate_trendline_mixed_positive_negative():
    """Test the /fit_trendline/ POST endpoint with mixed positive/negative data."""
    payload = {
        "timestamps": [2000, 2001, 2002, 2003, 2004],
        "data": [-5.0, -2.5, 0.0, 2.5, 5.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["slope"] == 2.5
    assert result["r_squared"] == 1.0


def test_calculate_trendline_negative_timestamps():
    """Test the /fit_trendline/ POST endpoint with negative timestamps."""
    payload = {
        "timestamps": [-2, -1, 0, 1, 2],
        "data": [10.0, 12.0, 14.0, 16.0, 18.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["slope"] == 2.0


def test_calculate_trendline_very_large_numbers():
    """Test the /fit_trendline/ POST endpoint with very large numbers."""
    payload = {
        "timestamps": [2000, 2001, 2002, 2003, 2004],
        "data": [1000000.0, 2000000.0, 3000000.0, 4000000.0, 5000000.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["slope"] == 1000000.0
    assert result["r_squared"] == 1.0


def test_calculate_trendline_all_zeros():
    """Test the /fit_trendline/ POST endpoint with all zero values."""
    payload = {
        "timestamps": [2000, 2001, 2002, 2003],
        "data": [0.0, 0.0, 0.0, 0.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result["slope"] == 0.0


def test_calculate_trendline_duplicate_timestamps():
    """Test the /fit_trendline/ POST endpoint with duplicate timestamps."""
    payload = {
        "timestamps": [2000, 2000, 2001, 2001],
        "data": [10.0, 12.0, 14.0, 16.0]
    }
    response = client.post("/fit_trendline/", json=payload)
    # Should still work - regression doesn't require unique x values
    assert response.status_code == 200


def test_say_hello_empty_string():
    """Test the /say_hello/{name} endpoint with empty string (edge case)."""
    response = client.get("/say_hello/")
    # FastAPI might handle this differently
    assert response.status_code == 404  # No route matches


def test_say_hello_with_spaces():
    """Test the /say_hello/{name} endpoint with spaces (URL encoded)."""
    response = client.get("/say_hello/John%20Doe")
    assert response.status_code == 200
    assert response.json() == {"Hello": "John Doe"}


def test_say_hello_very_long_name():
    """Test the /say_hello/{name} endpoint with very long name."""
    long_name = "A" * 1000
    response = client.get(f"/say_hello/{long_name}")
    assert response.status_code == 200
    assert response.json() == {"Hello": long_name}


def test_calculate_country_trendline_with_spaces():
    """Test the /country_trendline/{country} endpoint with country containing spaces."""
    response = client.get("/country_trendline/New%20Zealand")
    assert response.status_code == 200
    result = response.json()
    assert "slope" in result
    assert "r_squared" in result
