from app.extensions import db, ma
import os


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': os.getenv("DATABASE_SCHEMA_NAME")}  # Define the schema for the table

    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(50), nullable=False)

    def __init__(self, user_email, user_role):
        self.user_email = user_email
        self.user_role = user_role


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # To deserialize into model instance
