import pytest
from unittest.mock import patch, MagicMock
from src.extract.weather_api import WeatherAPI


def test_get_weather_data_success():
    """Test successful API call."""

    fake_response = {
        "name": "Warsaw",
        "main": {"temp": 273.15, "humidity": 85, "pressure": 1013},
        "dt": 1706216400,
        "wind": {"speed": 5.5},
    }

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_response
        mock_get.return_value = mock_response

        api = WeatherAPI()
        result = api.get_weather_data(["Warsaw"])

        assert len(result) == 1
        assert result[0]["name"] == "Warsaw"
        assert result[0]["main"]["temp"] == 273.15

        mock_get.assert_called_once()
