import pytest
from app.models.weather_data import WeatherData
from app.models.weather_stats import WeatherStats
from app import db, create_app
from app.controllers.weather_analytics_controller import WeatherAnalyticsController
import pytest


# Define the app fixture
@pytest.fixture
def app():
    """Fixture for setting up the Flask application context."""
    app = create_app()
    with app.app_context():
        yield app

class TestWeatherAnalyticsController:
    @pytest.fixture
    def sample_weather_data(self, app):
        """Fixture for creating sample weather data."""
        with app.app_context():
            weather1 = WeatherData(station_id="STN001", date="2023-01-01", max_temp=300, min_temp=150, precipitation=20)
            weather2 = WeatherData(station_id="STN001", date="2023-01-02", max_temp=310, min_temp=160, precipitation=25)
            db.session.add_all([weather1, weather2])
            db.session.commit()
            yield
            # Clean up
            db.session.query(WeatherData).delete()
            db.session.commit()

    @pytest.fixture
    def sample_weather_stats_data(self, app):
        """Fixture for creating sample weather stats data."""
        with app.app_context():
            stats1 = WeatherStats(station_id="STN001", year=2023, avg_max_temp=305, avg_min_temp=155, total_precipitation=45)
            db.session.add(stats1)
            db.session.commit()
            yield
            # Clean up
            db.session.query(WeatherStats).delete()
            db.session.commit()

    def test_fetch_weather_data_for_date(self, sample_weather_data):
        """Test fetch weather data for a specific date."""
        controller = WeatherAnalyticsController()
        data = controller.fetch_weather_data_for_date(station_id="STN001", date="2023-01-01", page=1, per_page=20)
        
        assert len(data) == 1  # We expect only one record for the given date
        assert data[0]["station_id"] == "STN001"
        assert data[0]["date"] == "2023-01-01"
        assert data[0]["max_temp"] == 30.0  # max_temp (300 / 10)
        assert data[0]["min_temp"] == 15.0  # min_temp (150 / 10)
        assert data[0]["precipitation"] == 2.0  # precipitation (20 / 10)
