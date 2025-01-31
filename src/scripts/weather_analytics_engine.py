import os, sys
from dataclasses import dataclass
from contextlib import contextmanager
from dotenv import find_dotenv, load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DatabaseError
import logging.handlers

# Configure root logger first
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('WeatherAnalyzer')

@dataclass
class DbConfig:
    connection_string: str
    results_table: str = "weather_stats"

class MeteorologicalProcessor:
    """Transforms raw weather observations into aggregated statistics"""
    
    def __init__(self, config: DbConfig):
        self._db_cfg = config
        self._db_engine = create_engine(config.connection_string)
        log.addHandler(logging.StreamHandler(sys.stdout))
        log.setLevel(logging.INFO)

    @contextmanager
    def _db_session(self):
        """Managed database connection context"""
        try:
            with self._db_engine.connect() as conn:
                yield conn
        except DatabaseError as db_err:
            log.critical("Database connection failed: %s", db_err)
            raise RuntimeError("Database unavailable") from db_err

    def _fetch_weather_data(self) -> pd.DataFrame:
        """Retrieve aggregated meteorological measurements"""
        analysis_query = text("""
            SELECT 
                station_id AS site_id,
                EXTRACT(YEAR FROM date) AS year,
                AVG(max_temp)/10 AS mean_max_temp,
                AVG(min_temp)/10 AS mean_min_temp,
                SUM(precipitation)/100 AS total_precipitation
            FROM weather_data
            GROUP BY 1, 2
            ORDER BY 1, 2
        """)
        
        log.info("Retrieving historical weather records")
        with self._db_session() as session:
            return pd.read_sql(analysis_query, session)

    def _save_weather_stats(self, metrics: pd.DataFrame) -> None:
        """Persist calculated statistics to database"""
        if metrics.empty:
            log.warning("No statistics available for storage")
            return
            
        log.info("Storing %d weather metrics in %s", 
                len(metrics), self._db_cfg.results_table)
        try:
            with self._db_session() as session:
                metrics.to_sql(
                    name=self._db_cfg.results_table,
                    con=session,
                    if_exists='replace',
                    index=False,
                    method='multi'
                )
            log.info("Weather metrics committed successfully")
        except DatabaseError as db_err:
            log.error("Metrics storage failed: %s", db_err)
            raise

    def generate_statistics(self) -> None:
        """Execute complete statistics generation workflow"""
        try:
            log.info("Initiating meteorological analysis")
            observations = self._fetch_weather_data()
            
            if not observations.empty:
                self._save_weather_stats(observations)
                log.info("Analysis process completed")
            else:
                log.warning("No observational data available")
                
        except Exception as analysis_error:
            log.error("Processing failure: %s", analysis_error)
            raise

def main():
    """Entry point for weather analysis system"""
    load_dotenv(find_dotenv(usecwd=True))
    
    db_uri = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:123@localhost:5432/weather_db'
    )
    
    config = DbConfig(
        connection_string=db_uri,
        results_table="weather_stats"
    )
    
    try:
        processor = MeteorologicalProcessor(config)
        processor.generate_statistics()
    except KeyboardInterrupt:
        log.info("Processing halted by user")
    except Exception as fatal_error:
        log.critical("System failure: %s", fatal_error)
        sys.exit(1)

if __name__ == "__main__":
    main()