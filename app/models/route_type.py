from app.extensions import db, ma
import os


class RouteType(db.Model):
    __tablename__ = 'route_types'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    route_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_type_name = db.Column(db.String(100), nullable=False)

    def __init__(self, route_type_name):
        self.route_type_name = route_type_name


class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RouteType
        load_instance = True  # To deserialize into model instance
