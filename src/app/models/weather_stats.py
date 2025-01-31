from app import db

class WeatherStats(db.Model):
    """Stores precomputed yearly weather statistics for stations"""
    __tablename__ = 'weather_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Float)      # In degrees Celsius
    avg_min_temp = db.Column(db.Float)      # In degrees Celsius
    total_precipitation = db.Column(db.Float)  # In centimeters

    # Unique constraint for station-year combination
    __table_args__ = (
        db.UniqueConstraint('station_id', 'year', name='unique_station_year'),
    )

    def __repr__(self):
        return f'<WeatherStats {self.station_id} {self.year}>'