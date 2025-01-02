from connexion import FlaskApp
from app.extensions import db, ma
from dotenv import load_dotenv

flask_app_instance = None


def create_app():
    global flask_app_instance

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

    # Save the app instance globally
    flask_app_instance = flask_app

    with flask_app.app_context():
        # Preload or prepare any needed resources here
        pass

    return app
