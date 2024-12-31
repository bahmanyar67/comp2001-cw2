from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase


# Base class for all models
class Base(DeclarativeBase):
    pass


# Initialize SQLAlchemy and Marshmallow
ma = Marshmallow()
db = SQLAlchemy(model_class=Base)
