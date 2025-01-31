import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"postgresql://postgres:123@host.docker.internal:5432/weather_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True