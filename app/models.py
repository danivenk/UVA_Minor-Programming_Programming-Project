#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
models.py defines all used models and has 1 event_listener for the password
Dani van Enk, 11823526

references:
    https://flask-login.readthedocs.io/en/latest/
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
    https://cs50.harvard.edu/web/notes/4/
"""

# used imports
from flask_sqlalchemy import SQLAlchemy, event
from flask_login import AnonymousUserMixin

# define SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    """
    The User Class defines a user admin and is based of db.Model

    tablename: users

    columns:
        id          - user id;
        first_name  - first name of the user;
        last_name   - last name of the user;
        password    - password of the user;
        username    - username of the user;
        admin       - has user admin privileges;
        orders      - orders of the user;

    methods:
        get_id          - gets the id of the user;
        items_in_cart   - checks the number of items in the user's cart;

    properies:
        is_authenticated
        is_active
        is_anonymous
    """

    # database tablename and column setup
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        """
        returns the id of the user
        """

        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        """
        returns the representation of the User class
        """

        return self.username


class AnonymousUser(AnonymousUserMixin):
    """
    The AnonymousUser Class defines a anonymous user and
    is a based of AnonymousUserMixin

    properies:
        admin - no admin privileges for anonymous users;
    """

    @property
    def admin(self):
        return False


stop_line = db.Table('stop_line_association',
                     db.Column('stop_id', db.ForeignKey('stops.id'),
                               primary_key=True),
                     db.Column('line_id', db.ForeignKey('lines.id'),
                               primary_key=True)
                     )


class Stop(db.Model):
    __tablename__ = "stops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=True)
    lines = db.relationship("Line", secondary=stop_line)

    def get_neighbouring_stops(self):
        neighbours = dict()

        for line in self.lines:
            for i, stop in enumerate(line.stops):
                if stop == self and (i <= 0):
                    neighbours[line.name] = \
                        {"previous": None, "next": line.stops[i+1]}
                elif stop == self and (i >= len(line.stops) - 1):
                    neighbours[line.name] = \
                        {"previous": line.stops[i-1], "next": None}
                elif stop == self:
                    neighbours[line.name] = \
                        {"previous": line.stops[i-1], "next": line.stops[i+1]}

        return neighbours

    def __repr__(self):
        return self.name


class Line(db.Model):
    __tablename__ = "lines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    stops = db.relationship("Stop", secondary=stop_line)

    def __repr__(self):
        return self.name + " Line"
