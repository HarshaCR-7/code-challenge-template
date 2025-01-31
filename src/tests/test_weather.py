import pytest
from unittest.mock import patch
from app import create_app
from flask import jsonify

@pytest.fixture
def app():
    app = create_app()  # assuming you have a 'testing' config for the app
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# Mocked data for weather data and statistics
mock_weather_data = [
    {
        "station_id": "STN001",
        "date": "2025-01-01",
        "max_temp": 30.0,
        "min_temp": 25.0,
        "precipitation": 50.0
    }
]

mock_weather_stats = [
    {
        "station_id": "STN001",
        "year": 2025,
        "avg_max_temp": 28.5,
        "avg_min_temp": 20.5,
        "total_precipitation": 120.0
    }
]

def test_fetch_weather_data_for_date(client):
    """Test fetching weather data based on station and date with mocked data."""
    
    # Mock the controller method
    with patch("app.controllers.weather_analytics_controller.WeatherAnalyticsController.fetch_weather_data_for_date") as mock_method:
        mock_method.return_value = mock_weather_data
        
        response = client.get('/api/weather/?station_id=STN001&date=2025-01-01')  # with trailing slash

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['station_id'] == 'STN001'
        assert data[0]['date'] == '2025-01-01'
        assert data[0]['max_temp'] == 30.0
        assert data[0]['min_temp'] == 25.0
        assert data[0]['precipitation'] == 50.0

def test_fetch_weather_data_missing_station_or_date(client):
    """Test error handling when neither station_id nor date is provided."""
    response = client.get('/api/weather/')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'At least one of station_id or date is required.'

def test_fetch_aggregated_weather_statistics(client):
    """Test fetching aggregated weather statistics based on station and year with mocked data."""
    
    # Mock the controller method
    with patch("app.controllers.weather_analytics_controller.WeatherAnalyticsController.fetch_aggregated_weather_statistics") as mock_method:
        mock_method.return_value = mock_weather_stats
        
        response = client.get('/api/weather/statistics?station_id=STN001&year=2025')  # For weather statistics

        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['station_id'] == 'STN001'
        assert data[0]['year'] == 2025
        assert data[0]['avg_max_temp'] == 28.5
        assert data[0]['avg_min_temp'] == 20.5
        assert data[0]['total_precipitation'] == 120.0

def test_fetch_weather_data_with_pagination(client):
    """Test paginated results for weather data with mocked data."""
    
    # Mock the controller method
    with patch("app.controllers.weather_analytics_controller.WeatherAnalyticsController.fetch_weather_data_for_date") as mock_method:
        mock_method.return_value = mock_weather_data
        
        response = client.get('/api/weather/?station_id=STN001&per_page=1&page=1')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1  # Only one record returned per page

def test_fetch_weather_statistics_with_pagination(client):
    """Test paginated results for weather statistics with mocked data."""
    
    # Mock the controller method
    with patch("app.controllers.weather_analytics_controller.WeatherAnalyticsController.fetch_aggregated_weather_statistics") as mock_method:
        mock_method.return_value = mock_weather_stats
        
        response = client.get('/api/weather/statistics?station_id=STN001&year=2025&per_page=1&page=1')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1  # Only one record returned per page
