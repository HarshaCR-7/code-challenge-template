import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scripts.weather_analytics_engine import MeteorologicalProcessor, DbConfig  # replace with the actual import path

class TestMeteorologicalProcessor(unittest.TestCase):

    @patch.object(MeteorologicalProcessor, '_save_weather_stats')
    @patch.object(MeteorologicalProcessor, '_fetch_weather_data', return_value=pd.DataFrame({
        'site_id': ['A', 'B'],
        'year': [2020, 2021],
        'mean_max_temp': [30.5, 32.1],
        'mean_min_temp': [15.5, 16.2],
        'total_precipitation': [100, 150]
    }))
    def test_save_weather_stats(self, mock_fetch_weather_data, mock_save_weather_stats):
        # Test if valid weather data gets saved
        config = DbConfig(connection_string="postgresql://test:test@localhost:5432/test_db")
        processor = MeteorologicalProcessor(config)
        
        processor.generate_statistics()  # Should call _save_weather_stats
        
        mock_save_weather_stats.assert_called_once()  # Ensure save was called

if __name__ == '__main__':
    unittest.main()
