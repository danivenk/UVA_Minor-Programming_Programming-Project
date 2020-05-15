import os
import sys
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

# define SQLAlchemy
db = SQLAlchemy()


def create_app():

    # Configure Flask app
    flask_app = Flask(__name__, root_path=os.getcwd())

    # Configure database
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with flask_app.app_context():
        db.init_app(flask_app)

    return flask_app


if __name__ == "__package__":
    sys.path.append(os.path.abspath(os.getcwd() + "/../"))

    import app.models
    import app.functions.search
    import app.functions.security
