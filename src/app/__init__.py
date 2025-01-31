from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api

db = SQLAlchemy()
ma = Marshmallow()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)

    # Initialize the API with Swagger UI at '/swagger/'
    api = Api(app, doc="/swagger/", title="Weather API", version="1.0", description="API for weather data analysis")

    # Import the namespace after initializing the Api
    from app.routes.weather import weather_ns

    # Register the namespace with the API under the '/api/weather' path
    api.add_namespace(weather_ns, path="/api/weather")

    return app