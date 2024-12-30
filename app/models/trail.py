from app.extensions import db, ma
from sqlalchemy import event
import datetime
import os


class Trail(db.Model):
    __tablename__ = 'trails'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_name = db.Column(db.String(100), nullable=False)
    trail_summary = db.Column(db.String(None), nullable=False)
    trail_description = db.Column(db.String(None))
    trail_owner_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DATABASE_SCHEMA_NAME')}.users.user_id"), nullable=False)
    trail_route_type_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DATABASE_SCHEMA_NAME')}.route_types.route_type_id"), nullable=False)
    trail_surface_type_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DATABASE_SCHEMA_NAME')}.surface_types.surface_type_id"), nullable=False)
    trail_location_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DATABASE_SCHEMA_NAME')}.locations.location_id"), nullable=False)
    trail_street = db.Column(db.String(255))
    trail_postal_code = db.Column(db.String(20))
    trail_county_id = db.Column(db.Integer, db.ForeignKey(f"{os.getenv('DATABASE_SCHEMA_NAME')}.counties.county_id"))
    trail_city = db.Column(db.String(100))
    trail_length = db.Column(db.Float)
    trail_length_unit = db.Column(db.String(20))
    trail_elevation_gain = db.Column(db.Float)
    trail_elevation_gain_unit = db.Column(db.String(20))
    trail_starting_point_lat = db.Column(db.Float)
    trail_starting_point_long = db.Column(db.Float)
    trail_ending_point_lat = db.Column(db.Float)
    trail_ending_point_long = db.Column(db.Float)
    trail_difficulty = db.Column(db.String(50))
    trail_created_at = db.Column(db.DateTime, server_default=db.func.now())
    trail_updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=datetime.datetime.now())

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@event.listens_for(Trail, 'before_update')
def receive_before_update(mapper, connection, target):
    target.trail_updated_at = datetime.datetime.now()


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True  # To deserialize into model instance
