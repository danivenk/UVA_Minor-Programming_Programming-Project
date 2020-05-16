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

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker


def main(argv):
    if len(argv) != 1:
        print("usage python load_data.py <dataset_name>")
        print("<dataset_name> is the name of the dataset")
        print("the used datafiles are data/<dataset_name>_stops.csv, "
              "data/<dataset_name>_lines.csv & "
              "data/<dataset_name>_companies.csv")

    add_stops(argv[0])
    lines = add_lines(argv[0])
    companies = add_companies(argv[0])

    for company_dict in companies.values():
        company = ssess.query(Company).filter_by(name=company_dict["name"]) \
            .first()
        company_lines = []
        for line_name in company_dict["lines"]:
            line = ssess.query(Line).filter(Line.name == line_name).first()
            company_lines.append(line)

        company.lines = company_lines
        ssess.add(company)
        ssess.commit()

    for line_dict in lines.values():
        line_company = ssess.query(Company) \
            .filter(Company.short_name == line_dict["company"]).first()
        line = ssess.query(Line) \
            .filter(and_(Line.name == line_dict["name"],
                         Line.company == line_company)).first()

        line_stops = []

        for stop_name in line_dict["stops"]:
            stop = ssess.query(Stop).filter(Stop.name == stop_name).first()
            line_stops.append(stop)

        stops_order = ""

        for i, stop in enumerate(line_stops):
            if i < len(line_stops) - 1:
                stops_order += f"{stop};"
            else:
                stops_order += f"{stop}"

        line.stops = line_stops
        line.stops_order = stops_order
        ssess.add(line)
        ssess.commit()


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
            stops[row[0]]["lines"]
        except KeyError:
            stops[row[0]]["lines"] = row[1].split(";")

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
            companies[row[0]]["lines"]
        except KeyError:
            companies[row[0]]["lines"] = []

        companies[row[0]]["lines"].append(row[2])

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
            lines[row[0]]["stops"]
        except KeyError:
            lines[row[0]]["stops"] = []

        lines[row[0]]["stops"].append(row[1])

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
