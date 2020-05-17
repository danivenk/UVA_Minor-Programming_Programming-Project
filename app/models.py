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

from .functions import security as s

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


# association table between stops and lines
stop_line = db.Table('stop_line_association', db.Model.metadata,
                     db.Column('stop_id', db.ForeignKey('stops.id',),
                               primary_key=True),
                     db.Column('line_id', db.ForeignKey('lines.id'),
                               primary_key=True),
                     db.UniqueConstraint('stop_id', 'line_id',
                                         name='UC_stop_id_line_id')
                     )


class Stop(db.Model):
    """
    The Stop Class defines a stop and is based of db.Model

    tablename: stops

    columns:
        id          - stop id;
        name        - name of the stop;
        stopnumber  - stopnames of the stop;
        location    - location of the stop;
        stoptype    - stoptype of the stop;
        lines       - lines of the stop;

    methods:
        get_stopnumbers         - get the stopnumber per line as dict;
        get_neighbouring_stops  - get neighbouring stops for this
                                    stop per stoptype;
    """

    # database tablename and column setup
    __tablename__ = "stops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    stopnumber = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    stoptype = db.Column(db.String, nullable=True)
    lines = db.relationship("Line", secondary=stop_line,
                            back_populates="stops", lazy="joined")

    def get_stopnumbers(self):
        """
        get the stopnumber per line as a dictionary

        return stopnumber dictionary
        """

        # predefine stopnumber dictionary
        stopnumbers = dict()

        # loop over stopnumber in stopnumbers
        for stopnumber in self.stopnumber.split(";"):

            # loop over line in lines
            for line in self.lines:

                # loop over prefix in prefix of the line
                for prefix in line.stopnumber_prefix.split(";"):

                    # no duplicates
                    if prefix in stopnumber:
                        stopnumbers[line] = stopnumber

        return stopnumbers

    def get_neighbouring_stops(self):
        """
        get neighbouring stops per stoptype

        returns dictionary with neighbouring stops
        """

        # predefine neighbours dictionaries
        neighbours = dict()

        # loop over line in lines
        for line in self.lines:

            # predefine neighbour dictionary per line
            neighbours[line] = dict()

            # loop over stops and stoptype in line
            for _type, stops in line.get_stops()[0].items():

                # loop over index and stop in stops
                for i, stop in enumerate(stops):

                    # add previous and next stop to neighbours
                    #   none if no neighbour is found
                    if stop == self and (i <= 0):
                        neighbours[line][_type] = \
                            {"previous": None, "next": stops[i+1]}
                    elif stop == self and (i >= len(stops) - 1):
                        neighbours[line][_type] = \
                            {"previous": stops[i-1], "next": None}
                    elif stop == self:
                        neighbours[line][_type] = \
                            {"previous": stops[i-1],
                             "next": stops[i+1]}

        return neighbours

    def __repr__(self):
        return self.name


class Line(db.Model):
    """
    The Line Class defines a line and is based of db.Model

    tablename: lines

    columns:
        id                  - line id;
        name                - name of the line;
        stops               - stopnames of the line;
        stops_order         - order of stops of line;
        stopnumber_prefix   - stopnumber prefix of the line;
        stoptypes           - stoptype of line;
        company_id          - company id of line;
        company             - company of line;

    methods:
        get_stop                    - gets stops in right order and
                                        stops per stopstype;
        check_stopnumber_prefix     - check stopnumber prefix;
    """

    # database tablename and column setup
    __tablename__ = "lines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    stops = db.relationship("Stop", secondary=stop_line,
                            back_populates="lines", lazy="joined")
    stops_order = db.Column(db.String, nullable=True)
    stopnumber_prefix = db.Column(db.String, nullable=True)
    stoptypes = db.Column(db.String, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    company = db.relationship("Company", uselist=False)

    def get_stops(self):
        """
        get stops in correct order and stops per stoptype

        return stops in correct order and stops per stoptype
        """

        # predefine stops dictionary and stops full width dictionary
        stops = dict()
        stops_full_width = dict()

        stops_order = self.stops_order.split(";")

        correct_order = []

        for stop_order in stops_order:
            for stop in self.stops:
                if stop.name == stop_order:
                    correct_order.append(stop)

        for _type in self.stoptypes.split(";"):
            stops[_type] = []
            stops_full_width[_type] = []

            for stop in correct_order:
                if _type in stop.stoptype.split(";"):
                    stops[_type].append(stop)
                    stops_full_width[_type].append(stop)
                else:
                    stops_full_width[_type].append(None)

        return stops, stops_full_width, correct_order

    def check_stopnumber_prefix(self, prefix):

        for stop_prefix in self.stopnumber_prefix.split(";"):
            if stop_prefix in prefix:
                return True

        return False

    def __repr__(self):
        if self.company:
            return f"{self.company.short_name} {self.name} Line"
        else:
            return self.name + " Line"


class Company(db.Model):
    # database tablename and column setup
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    short_name = db.Column(db.String, nullable=True)
    lines = db.relationship("Line")

    def __repr__(self):
        return self.name


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    """
    listens for a change in the password of a user
    if called it hashes the new password (if password is changed)

    references:
        https://stackoverflow.com/a/57100627
    """

    if value != oldvalue:
        return s.hash_psswd(value)
    return value
