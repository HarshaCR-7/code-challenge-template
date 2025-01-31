from flask_restx import Resource, Namespace
from flask import request, jsonify, make_response
from app.controllers.weather_analytics_controller import WeatherAnalyticsController

weather_ns = Namespace("weather", description="Operations related to weather data analysis")


@weather_ns.route("/")
class WeatherDataResource(Resource):
    """
    Retrieves weather data for a specified station and date.
    """

    @weather_ns.param("station_id", "Unique identifier of the weather station", type=str, required=False)
    @weather_ns.param("date", "Requested date in ISO format (YYYY-MM-DD)", type=str, required=False)
    @weather_ns.param("per_page", "Page number for paginated results", type=int, default=20)
    @weather_ns.param("page", "Page number for paginated results", type=int, default=1)
    def get(self):
        """
        Fetch weather data based on station ID and date.
        
        Returns:
            dict: Weather details for the specified parameters with HTTP status 200.
        """
        station_id = request.args.get("station_id")
        date = request.args.get("date")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        # Check if at least one of station_id or date is provided
        if not station_id and not date:
            return make_response(jsonify({"error": "At least one of station_id or date is required."}), 400)

        weather_data = WeatherAnalyticsController().fetch_weather_data_for_date(station_id, date, page, per_page)
        return make_response(jsonify(weather_data), 200)


@weather_ns.route("/statistics")
class WeatherStatisticsResource(Resource):
    """
    Provides aggregated weather statistics for a given station and year.
    """
    
    @weather_ns.param("station_id", "Unique identifier of the weather station", type=str, required=False)
    @weather_ns.param("year", "Year for statistical analysis", type=int, required=False)
    @weather_ns.param("page", "Page number for paginated results", type=int, default=1)
    @weather_ns.param("per_page", "Page number for paginated results", type=int, default=20)
    def get(self):
        """
        Retrieve weather statistics for a specific station and year.
        
        Returns:
            dict: Aggregated weather statistics with HTTP status 200.
        """
        station_id = request.args.get("station_id")
        year = request.args.get("year", type=int)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        stats_data = WeatherAnalyticsController().fetch_aggregated_weather_statistics(station_id, year, page, per_page)
        return make_response(jsonify(stats_data), 200)
