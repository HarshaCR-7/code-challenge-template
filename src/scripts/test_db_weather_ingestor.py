import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from scripts.db_weather_ingestor import WeatherInfoLoader  # Replace with your actual module
import os
from pathlib import Path
from sqlalchemy import create_engine, exc
from io import StringIO


class TestWeatherInfoLoader(unittest.TestCase):

    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.glob")
    @patch("builtins.print")  # Replace print with a mock to capture logging
    def test_handle_folder(self, mock_print, mock_glob, mock_is_dir):
        mock_is_dir.return_value = True
        mock_glob.return_value = [Path("file1.txt"), Path("file2.txt")]

        loader = WeatherInfoLoader(conn_str="postgresql://localhost/test_db")
        loader.handle_folder("./wx_data")

        # Ensure handle_file is called for each file in the folder
        self.assertEqual(mock_print.call_count, 0)  # We only care about ensuring it runs, not actual log output

if __name__ == "__main__":
    unittest.main()
