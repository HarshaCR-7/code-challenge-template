from app import db
from datetime import date


class WeatherData(db.Model):
    """Represents daily weather observations for weather stations"""
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Integer)        # In tenths of a degree Celsius
    min_temp = db.Column(db.Integer)        # In tenths of a degree Celsius
    precipitation = db.Column(db.Integer)   # In tenths of a millimeter

    # Unique constraint for station-date combination
    __table_args__ = (
        db.UniqueConstraint('station_id', 'date', name='unique_station_date'),
    )

    def __repr__(self):
        return f'<WeatherData {self.station_id} {self.date}>'
