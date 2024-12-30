from app.extensions import db, ma
import os


class County(db.Model):
    __tablename__ = 'counties'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    county_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    county_name = db.Column(db.String(100), nullable=False)

    def __init__(self, county_name):
        self.county_name = county_name


class CountySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = County
        load_instance = True  # To deserialize into model instance
