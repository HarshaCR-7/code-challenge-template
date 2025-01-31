from app.models.weather_data import WeatherData
from app.models.weather_stats import WeatherStats

class WeatherAnalyticsController:
    """
    This controller manages operations related to weather data retrieval and statistical analysis.
    It provides methods to fetch weather data for specific stations and dates, 
    and aggregate weather statistics for stations within a given year.
    """

    @staticmethod
    def fetch_aggregated_weather_statistics(station_id=None, year=None, page=1, per_page=20):
        """
        Retrieves aggregated weather statistics for a specific weather station in a given year.

        Args:
            station_id (str): The ID of the weather station.
            year (int): The year for which statistics are to be fetched.
            page (int): The page number for paginated results (default is 1).
            per_page (int): The number of records per page (default is 20).

        Returns:
            list: A list of dictionaries containing the aggregated weather statistics.
        """
        query = WeatherStats.query
        query = WeatherAnalyticsController._filter_by_station_and_year(query, station_id, year)
        
        return WeatherAnalyticsController._paginate_query(query, page, per_page, WeatherAnalyticsController._format_weather_stats)

    @staticmethod
    def fetch_weather_data_for_date(station_id=None, date=None, page=1, per_page=20):
        """
        Retrieves weather data for a specific weather station on a given date.

        Args:
            station_id (str): The ID of the weather station.
            date (str): The specific date for which weather data is required (ISO format).
            page (int): The page number for paginated results (default is 1).
            per_page (int): The number of results per page (default is 20).

        Returns:
            list: A list of dictionaries containing the weather data for the specified station and date.
        """
        query = WeatherData.query
        query = WeatherAnalyticsController._filter_by_station_and_date(query, station_id, date)
        
        return WeatherAnalyticsController._paginate_query(query, page, per_page, WeatherAnalyticsController._format_weather_data)

    @staticmethod
    def _filter_by_station_and_year(query, station_id, year):
        """
        Applies filters to the query to fetch data by station ID and year.
        
        Args:
            query: The query object.
            station_id (str): The weather station ID.
            year (int): The year for filtering data.
        
        Returns:
            query: The filtered query object.
        """
        if station_id:
            query = query.filter_by(station_id=station_id)
        if year:
            query = query.filter_by(year=year)
        return query

    @staticmethod
    def _filter_by_station_and_date(query, station_id, date):
        """
        Applies filters to the query to fetch data by station ID and date.
        
        Args:
            query: The query object.
            station_id (str): The weather station ID.
            date (str): The date for filtering data (ISO format).
        
        Returns:
            query: The filtered query object.
        """
        if station_id:
            query = query.filter_by(station_id=station_id)
        if date:
            query = query.filter_by(date=date)
        return query

    @staticmethod
    def _paginate_query(query, page, per_page, format_func):
        """
        Paginates the query and formats the data.
        
        Args:
            query: The query object to paginate.
            page (int): The page number.
            per_page (int): The number of results per page.
            format_func (function): The function to format the query result.
        
        Returns:
            list: A list of formatted results for the requested page.
        """
        data = query.paginate(page=page, per_page=per_page).items
        return format_func(data)

    @staticmethod
    def _format_weather_stats(data):
        """
        Formats the aggregated weather statistics data into a list of dictionaries.
        
        Args:
            data: The raw weather statistics data to format.
        
        Returns:
            list: The formatted weather statistics data.
        """
        return [
            {
                "station_id": s.station_id,
                "year": s.year,
                "avg_max_temp": s.avg_max_temp,
                "avg_min_temp": s.avg_min_temp,
                "total_precipitation": s.total_precipitation,
            }
            for s in data
        ]

    @staticmethod
    def _format_weather_data(data):
        """
        Formats the weather data for a given date into a list of dictionaries.
        
        Args:
            data: The raw weather data to format.
        
        Returns:
            list: The formatted weather data.
        """
        return [
            {
                "station_id": d.station_id,
                "date": d.date.isoformat(),
                "max_temp": d.max_temp / 10 if d.max_temp else None,
                "min_temp": d.min_temp / 10 if d.min_temp else None,
                "precipitation": d.precipitation / 10 if d.precipitation else None,
            }
            for d in data
        ]
