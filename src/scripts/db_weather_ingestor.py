import pathlib, os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, exc
import logging
from typing import Union

load_dotenv()


class WeatherInfoLoader:
    """Handles loading of weather observations into storage"""

    def __init__(self, conn_str: str, file_suffix: str = ".txt"):
        """
        :param conn_str: Storage connection string
        :param file_suffix: Data file extension
        """
        self.storage_link = conn_str
        self.destination = "weather_data"
        self.file_pattern = file_suffix
        self.db_adapter = create_engine(conn_str)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.log_handler = logging.getLogger(self.__class__.__name__)

    def _parse_weather_file(self, file_loc: str) -> Union[pd.DataFrame, None]:
        """
        :param file_loc: Path to weather data file
        :return: Processed dataframe or None
        """
        try:
            self.log_handler.info(f"Loading data from: {file_loc}")
            raw_df = pd.read_csv(
                file_loc,
                delimiter="\t",
                header=None,
                names=["date", "max_temp", "min_temp", "precipitation"],
            )

            raw_df["date"] = pd.to_datetime(
                raw_df["date"], format="%Y%m%d", errors="coerce"
            )
            raw_df["station_id"] = pathlib.Path(file_loc).stem
            processed_df = raw_df.replace(-9999, pd.NA)

            valid_records = processed_df.dropna(subset=["date"])
            self.log_handler.info(
                f"Completed processing {file_loc} | Valid entries: {len(valid_records)}"
            )
            return valid_records
        except Exception as err:
            self.log_handler.error(f"Failed processing {file_loc} | Reason: {err}")
            return None

    def _transfer_to_storage(self, weather_df: pd.DataFrame):
        """Transfers processed data to persistent storage"""
        try:
            record_count = weather_df.shape[0]
            self.log_handler.info(
                f"Attempting to insert {record_count} entries to {self.destination}"
            )
            with self.db_adapter.connect() as db_session:
                weather_df.to_sql(
                    self.destination,
                    db_session,
                    if_exists="append",
                    index=False,
                    method="multi",
                )
            self.log_handler.info(
                f"Successfully stored {record_count} entries in {self.destination}"
            )
        except exc.SQLAlchemyError as db_err:
            self.log_handler.error(f"Storage operation failed: {db_err}")

    def handle_file(self, file_path: str):
        """Orchestrates file processing pipeline"""
        processed_data = self._parse_weather_file(file_path)
        if processed_data is not None and not processed_data.empty:
            self._transfer_to_storage(processed_data)
        else:
            self.log_handler.warning(f"Empty dataset in {file_path}")

    def handle_folder(self, folder_path: str):
        """Processes all valid files in directory"""
        self.log_handler.info(f"Scanning directory: {folder_path}")
        if not pathlib.Path(folder_path).is_dir():
            self.log_handler.error(f"Invalid directory: {folder_path}")
            return

        file_list = [
            f for f in pathlib.Path(folder_path).glob(f"*{self.file_pattern}") if f.is_file()
        ]
        if not file_list:
            self.log_handler.warning(
                f"No {self.file_pattern} files found in {folder_path}"
            )
            return

        for weather_file in file_list:
            self.handle_file(str(weather_file))


if __name__ == "__main__":
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://weather_user:securepass@localhost:5432/weather_db"
    )
    SOURCE_FOLDER = "./wx_data"
    WEATHER_TABLE = "weather_data"

    loader = WeatherInfoLoader(conn_str=DATABASE_URL)
    loader.handle_folder(SOURCE_FOLDER)