from app.extensions import db, ma
import os


class Tag(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(255), nullable=False)

    def __init__(self, tag_name):
        self.tag_name = tag_name


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True  # To deserialize into model instance
