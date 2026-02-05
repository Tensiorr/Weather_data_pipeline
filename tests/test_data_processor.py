import pytest
from src.transform.data_processor import (
    kelvin_to_celsius,
    safe_get,
    transform_weather_data,
)
from datetime import datetime


def test_kelvin_to_celsius_freezing_point():
    """Test conversion at water freezing point."""
    result = kelvin_to_celsius(273.15)
    assert result == 0.0


def test_kelvin_to_celsius_absolute_zero():
    """Test conversion at absolute zero."""
    result = kelvin_to_celsius(0)
    assert result == -273.15


def test_kelvin_to_celsius_negative_value():
    """Negative Kelvin should raise ValueError."""
    with pytest.raises(ValueError, match="cannot be negative"):
        kelvin_to_celsius(-10)


def test_kelvin_to_celsius_with_none():
    """None should raise TypeError."""
    with pytest.raises(TypeError):
        kelvin_to_celsius(None)


def test_kelvin_to_celsius_with_string():
    """String should raise TypeError."""
    with pytest.raises(TypeError):
        kelvin_to_celsius("273.15")


def test_safe_get_simple_key():
    """Test getting a simple key."""
    data = {"city": "Warsaw", "temp": 15.5}
    result = safe_get(data, "city")
    assert result == "Warsaw"


def test_safe_get_nested_key():
    """Test getting nested keys."""
    data = {"main": {"temp": 273.15, "humidity": 85}}
    result = safe_get(data, "main", "temp")
    assert result == 273.15


def test_safe_get_wrong_key():
    """Test with wrong key."""
    data = {"city": "Warsaw", "temp": 15.5}
    result = safe_get(data, "test")
    assert result is None


def test_safe_get_wrong_first_key():
    """Test with wrong first key."""
    data = {"main": {"temp": 273.15, "humidity": 85}}
    result = safe_get(data, "test", "temp")
    assert result is None


def test_safe_get_wrong_nested_key():
    """Test with wrong nested key."""
    data = {"main": {"temp": 273.15, "humidity": 85}}
    result = safe_get(data, "main", "test")
    assert result is None


def test_safe_get_non_dict_value():
    """Test when intermediate value is not a dict."""
    data = {"main": "not_a_dict"}
    result = safe_get(data, "main", "temp")
    assert result is None


def test_safe_get_custom_default():
    """Test with custom default value."""
    data = {"city": "Warsaw"}
    result = safe_get(data, "temp", default=0)
    assert result == 0


def test_transform_weather_data_correct_dict():
    raw_data = {
        "name": "Warsaw",
        "main": {"temp": 273.15, "humidity": 85, "pressure": 1013},
        "dt": 1706216400,
        "wind": {"speed": 5.5},
    }

    expected_dt = datetime.fromtimestamp(1706216400)

    result = transform_weather_data(raw_data)
    assert result["city"] == "Warsaw"
    assert result["temperature_celsius"] == 0.0
    assert result["measurement_time"] == expected_dt
    assert result["humidity"] == 85
    assert result["pressure"] == 1013
    assert result["wind_speed"] == 5.5


def test_transform_weather_data_missing_city():
    """Should return None if city name is missing."""
    raw_data = {"main": {"temp": 273.15}, "dt": 1706216400}

    result = transform_weather_data(raw_data)
    assert result is None


def test_transform_weather_data_missing_timestamp():
    """Should return None if timestamp is missing."""
    raw_data = {
        "name": "Warsaw",
    }

    result = transform_weather_data(raw_data)
    assert result is None


def test_transform_weather_data_partial_data():
    """Should handle missing fields gracefully."""
    raw_data = {"name": "Warsaw", "main": {"temp": 273.15}, "dt": 1706216400}

    expected_dt = datetime.fromtimestamp(1706216400)

    result = transform_weather_data(raw_data)
    assert result["city"] == "Warsaw"
    assert result["temperature_celsius"] == 0.0
    assert result["measurement_time"] == expected_dt
    assert result["humidity"] is None
    assert result["pressure"] is None
    assert result["wind_speed"] is None
