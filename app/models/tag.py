from app.extensions import db, ma
import os
import app.models


class Tag(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {
        'schema': os.getenv("DATABASE_SCHEMA_NAME"),
        'extend_existing': True  # Prevent redefinition errors
    }

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(100), nullable=False)

    # relationships
    # trails = db.relationship('Trail', secondary='trail_tag', backref='Tag')

    def __init__(self, tag_name):
        self.tag_name = tag_name


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True  # To deserialize into model instance
