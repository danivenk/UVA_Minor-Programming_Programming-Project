#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
application.py defines flask application
Dani van Enk, 11823526
"""

import os
import shlex

from flask import Flask, abort, request, render_template, session, escape, \
                  redirect
from flask_session import Session
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.exceptions import default_exceptions, HTTPException

from sqlalchemy import or_

from .models import db, User, AnonymousUser, Stop, Line, Company
from .adminviews import AdminUserIndexView, AdminView, NetworkView
from .functions.search import relevance_query
from .functions import security

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
admin = Admin(app, index_view=AdminUserIndexView(),
              base_template="admin/master.html")
admin.add_view(AdminView(User, db.session))
admin.add_view(NetworkView(Stop, db.session))
admin.add_view(NetworkView(Line, db.session))
admin.add_view(NetworkView(Company, db.session))

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


@app.template_test("line")
def line_test(obj):
    return type(obj) is Line


@app.template_test("stop")
def stop_test(obj):
    return type(obj) is Stop


@app.route("/", methods=["GET"])
def index():

    if request.method not in request.url_rule.methods:
        abort(405)

    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():

    if request.method not in request.url_rule.methods:
        abort(405)

    search_query = request.args.get('search', None)
    queries = shlex.split(search_query)
    query_list = relevance_query(queries)

    result_list = []

    for query in query_list:
        result_stops = Stop.query.filter(or_(Stop.name.ilike(f"%{query}%"),
                                             Stop.location.ilike(f"%{query}%")
                                             )).all()
        result_lines = Line.query.filter(Line.name.ilike(f"%{query}%")).all()

        for stop in result_stops:
            if stop not in result_list:
                result_list.append(stop)

        for line in result_lines:
            if line not in result_list:
                result_list.append(line)

    return render_template("search.html", results=result_list,
                           query=search_query)


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

    return render_template("line.html", current_line=current_line)


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

    return render_template("stop.html", current_stop=current_stop)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    register a new user

    aborts if:
        - a user is already registering (403)
        - no username/password/retype password is given (400)
        - user already registered (400)
        - request is anything else than "POST" or "GET" (405)

    returns the register form again if the retype password and password
        weren't the same or the request was a "GET" request. If
        registration was successfull it redirects (303) to "/".
    """

    next_page = request.args.get("page", None)

    # abort using a 405 if request method is not "POST" or "GET"
    if request.method not in request.url_rule.methods:
        abort(405)

    if request.method == "POST":
        # check if user is already registering if so abort 403
        if session.get("register_user") is not None:

            # remove registering user from session
            session.pop("register_user", None)
            abort(403, "Detected double submission of form please try "
                  "again")

        # get all values from the submitted form
        username = escape(request.form.get("register_username"))
        password = escape(request.form.get("register_password"))
        rpassword = escape(request.form.get("register_rpassword"))
        email = escape(request.form.get("register_email"))

        # if the given passwords aren't the same rerender the template
        if password != rpassword:
            return render_template("register.html",
                                   message="passwords weren't the same...")

        # if no username/password/retype password were given abort (400)
        if not username or not password or not rpassword:

            # abort using a 400 HTTPException
            abort(400, "No username/password specified")

        # add registering user to session
        session["register_user"] = username

        # look for username in database
        user = User.query.filter_by(username=username).all()

        # if username was found in the database abort (400)
        if len(user) >= 1:

            # abort using a 400 HTTPException
            abort(400, "User already registered")

        # add user to database
        register_user = User(password=password, username=username,
                             email=email)
        db.session.add(register_user)
        db.session.commit()

        # remove registering user from session
        session.pop("register_user", None)

        return redirect(next_page, 303)
    elif request.method == "GET":
        return render_template("register.html", last=next_page)


@app.route("/login", methods=["POST"])
def login():

    if request.method not in request.url_rule.methods:
        abort(405)

    # get the username and password from the login form
    username = escape(request.form.get("username"))
    password = escape(request.form.get("password"))
    next_page = escape(request.form.get("page"))

    # if no credentials are given abort using 400 HTTPException
    if not username or not password:

        abort(400, "No username/password specified")

    # look for user in database
    user_login = User.query.filter_by(username=username).first()

    # is user not found in database abort using 404 HTTPException
    if not user_login:

        abort(404, "Not found")

    # check if credentials are correct
    #   login if correct, abort using 403 HTTPException if not
    if security.compare_hash(user_login.password, password):
        login_user(user_login)
    else:
        abort(403)

    return redirect(next_page, 303)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    log logged on user out, LOGIN REQUIRED

    abort if:
        - request anything else than "GET";

    return redirect to index (303)
    """

    next_page = request.args.get("page", None)

    if request.method not in request.url_rule.methods:
        abort(405)

    # logout user
    logout_user()

    return redirect(next_page, 303)


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
