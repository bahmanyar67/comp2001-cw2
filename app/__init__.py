from connexion import FlaskApp
from app.extensions import db, ma
from dotenv import load_dotenv


def create_app():
    load_dotenv()

    app = FlaskApp(__name__, specification_dir="./")

    # Load Swagger API
    app.add_api("swagger.yml", arguments={"title": "Trail REST API"})

    # Access the Flask app instance
    flask_app = app.app

    # Configure the app
    flask_app.config.from_object("app.config.Config")


    # Initialize SQLAlchemy and Marshmallow
    db.init_app(flask_app)
    ma.init_app(flask_app)

    return app
