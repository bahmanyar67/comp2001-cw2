from app.extensions import db, ma
import os


class Location(db.Model):
    __tablename__ = 'locations'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(255), nullable=False)

    def __init__(self, location_name):
        self.location_name = location_name


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True  # To deserialize into model instance
