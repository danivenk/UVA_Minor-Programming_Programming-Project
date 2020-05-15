#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
models.py defines all used models and has 1 event_listener for the password
Dani van Enk, 11823526
"""

import sys
import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def main(argv):
    if len(argv) != 1:
        print("usage python load_data.py <dataset_name>")
        print("<dataset_name> is the name of the dataset")
        print("the used datafiles are data/<dataset_name>_stops.csv, "
              "data/<dataset_name>_lines.csv & "
              "data/<dataset_name>_companies.csv")

    stops = add_stops(argv[0])
    lines = add_lines(argv[0])
    companies = add_companies(argv[0])


def add_stops(dataset_name):
    datafile_stops = open(f"../data/{dataset_name}_stops.csv", "r",
                          encoding="utf-8")
    stops_file = csv.reader(datafile_stops, delimiter=",")

    next(stops_file)

    stops = dict()

    for row in stops_file:

        try:
            stops[row[0]]
        except KeyError:
            stops[row[0]] = dict()

        stops[row[0]]["name"] = row[0]
        stops[row[0]]["stopnumber"] = row[2]
        stops[row[0]]["location"] = row[3]
        stops[row[0]]["stoptype"] = row[4]

        try:
            stops[row[0]]["line"]
        except KeyError:
            stops[row[0]]["line"] = row[1].split(";")

    for stop in stops.values():
        database_row = Stop(name=stop["name"], stopnumber=stop["stopnumber"],
                            location=stop["location"],
                            stoptype=stop["stoptype"])

        ssess.add(database_row)
        ssess.commit()

    return stops


def add_companies(dataset_name):
    datafile_companies = open(f"../data/{dataset_name}_companies.csv", "r",
                              encoding="utf-8")
    companies_file = csv.reader(datafile_companies, delimiter=",")

    next(companies_file)

    companies = dict()

    for row in companies_file:

        try:
            companies[row[0]]
        except KeyError:
            companies[row[0]] = dict()

        companies[row[0]]["name"] = row[0]
        companies[row[0]]["short_name"] = row[1]

        try:
            companies[row[0]]["line"]
        except KeyError:
            companies[row[0]]["line"] = []

        companies[row[0]]["line"].append(row[2])

    for company in companies.values():
        database_row = Company(name=company["name"],
                               short_name=company["short_name"])

        ssess.add(database_row)
        ssess.commit()

    return companies


def add_lines(dataset_name):
    datafile_lines = open(f"../data/{dataset_name}_lines.csv", "r",
                          encoding="utf-8")
    lines_file = csv.reader(datafile_lines, delimiter=",")

    next(lines_file)

    lines = dict()

    for row in lines_file:

        try:
            lines[row[0]]
        except KeyError:
            lines[row[0]] = dict()
        lines[row[0]]["name"] = row[0]
        lines[row[0]]["stopnumber_prefix"] = row[2]
        lines[row[0]]["stoptypes"] = row[3]
        lines[row[0]]["company"] = row[4]

        try:
            lines[row[0]]["stop"]
        except KeyError:
            lines[row[0]]["stop"] = []

        lines[row[0]]["stop"].append(row[1])

    for line in lines.values():
        database_row = Line(name=line["name"],
                            stopnumber_prefix=line["stopnumber_prefix"],
                            stoptypes=line["stoptypes"])

        ssess.add(database_row)
        ssess.commit()

    return lines


if __name__ == "__main__":
    # https://stackoverflow.com/a/16985066
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from app.models import db, Stop, Line, Company

    # Configure database
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")

    # set up database
    engine = create_engine(os.getenv("DATABASE_URL"))
    ssess = scoped_session(sessionmaker(bind=engine))
    db.metadata.create_all(engine)

    main(sys.argv[1:])
