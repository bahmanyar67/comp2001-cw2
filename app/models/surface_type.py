from app.extensions import db, ma
import os


class SurfaceType(db.Model):
    __tablename__ = 'surface_types'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    surface_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surface_type_name = db.Column(db.String(100), nullable=False)

    def __init__(self, surface_type_name):
        self.surface_type_name = surface_type_name


class SurfaceTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurfaceType
        load_instance = True  # To deserialize into model instance
