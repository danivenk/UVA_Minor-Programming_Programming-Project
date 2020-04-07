#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
application.py defines flask application
Dani van Enk, 11823526
"""

import os

from flask import Flask, abort, request
from flask_session import Session
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager

from models import db, User, AnonymousUser
from adminviews import AdminUserIndexView, AdminView

# Configure Flask app
app = Flask(__name__)

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

    if request.method == "GET":
        abort(405)

    return "Hello World"
