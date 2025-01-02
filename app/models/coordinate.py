from app.extensions import db, ma
import os


class Coordinate(db.Model):
    __tablename__ = 'coordinates'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    coordinate_id = db.Column(db.Integer, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DATABASE_SCHEMA_NAME')}.trails.trail_id"),
                         nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, trail_id, latitude, longitude):
        self.trail_id = trail_id
        self.latitude = latitude
        self.longitude = longitude


class CoordinateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Coordinate
        load_instance = True  # To deserialize into model instance
