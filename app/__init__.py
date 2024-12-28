from flask import render_template
from connexion import FlaskApp


def create_app():
    app = FlaskApp(__name__, specification_dir="./")

    # Load Swagger
    app.add_api("swagger.yml", arguments={"title": "Trail REST API"})

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
