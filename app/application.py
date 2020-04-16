#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
application.py defines flask application
Dani van Enk, 11823526
"""

import os

from flask import Flask, abort, request, render_template
from flask_session import Session
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
from werkzeug.exceptions import default_exceptions, HTTPException

from models import db, User, AnonymousUser, Stop, Line
from adminviews import AdminUserIndexView, AdminView, NetworkView

# Configure Flask app
app = Flask(__name__, root_path=os.getcwd())

# Configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.secret_key = os.environ['SECRET_KEY']

# Configure session, use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure migrations
Migrate(app, db)

# admin setup
admin = Admin(app, index_view=AdminUserIndexView())
admin.add_view(AdminView(User, db.session))
admin.add_view(NetworkView(Stop, db.session))
admin.add_view(NetworkView(Line, db.session))

# login setup
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    load a user into the login manager
    """

    user = User.query.get(user_id)
    if user:
        return user
    else:
        return None


@app.route("/", methods=["GET"])
def index():

    if request.method not in request.url_rule.methods:
        abort(405)

    return render_template("index.html")


@app.route("/lines", methods=["GET"])
def lines():

    if request.method not in request.url_rule.methods:
        abort(405)

    return render_template("lines.html", lines=Line.query.all())


@app.route("/line", methods=["GET"])
def line():

    if request.method not in request.url_rule.methods:
        abort(405)

    line_id = request.args.get('id', None)
    current_line = Line.query.get(line_id)

    return render_template("line.html", line=current_line)


@app.route("/stops", methods=["GET"])
def stops():

    if request.method not in request.url_rule.methods:
        abort(405)

    return render_template("stops.html", stops=Stop.query.all())


@app.route("/stop", methods=["GET"])
def stop():

    if request.method not in request.url_rule.methods:
        abort(405)

    stop_id = request.args.get('id', None)
    current_stop = Stop.query.get(stop_id)

    return render_template("stop.html", stop=current_stop)


@app.errorhandler(HTTPException)
def errorhandler(error):
    """
    Handle errors

    used same code as in the exercise similarities

    return error template

    reused part of the code from the Survey and Similarities web apps
        from UVA Mprog Programming 2 Module 10 - Web
    """

    # split the error into the header and message (index, 0 header, 1 text)
    error_message = str(error).split(":")

    return render_template("error.html", header=error_message[0],
                           message=error_message[1]), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
