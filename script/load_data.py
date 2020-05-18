#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
load_data.py loads the data from data/
    (only when the files have the correct name style)
Dani van Enk, 11823526
"""

# used imports
import sys
import os
import csv

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import scoped_session, sessionmaker


def main(argv):
    """
    main function of the code it submits the stops/lines and companies to
        the database and adds the correct connections
    """

    # check if 1 argument is given after the filename (load_data.py)
    if len(argv) != 1:
        print("usage python load_data.py <dataset_name>")
        print("<dataset_name> is the name of the dataset")
        print("the used datafiles are data/<dataset_name>_stops.csv, "
              "data/<dataset_name>_lines.csv & "
              "data/<dataset_name>_companies.csv")

    # add the stops/lines and companies
    add_stops(argv[0])
    lines = add_lines(argv[0])
    companies = add_companies(argv[0])

    # loop over all companies in companies (dict)
    for company_dict in companies.values():

        # find the current company
        company = ssess.query(Company).filter_by(name=company_dict["name"]) \
            .first()

        # predefine company_lines list
        company_lines = []

        # loop over lines in company_dict
        for line_name in company_dict["lines"]:

            # find line by name
            line = ssess.query(Line).filter(Line.name == line_name).first()

            # add line to company_lines
            company_lines.append(line)

        # add company_lines to lines attribute of company, update to database
        company.lines = company_lines
        ssess.add(company)
        ssess.commit()

    # loop over all lines in lines (dict)
    for line_dict in lines.values():

        # find the company of current line by shortname
        line_company = ssess.query(Company) \
            .filter(Company.short_name == line_dict["company"]).first()

        # find line by line name and company
        line = ssess.query(Line) \
            .filter(and_(Line.name == line_dict["name"],
                         Line.company == line_company)).first()

        # predefine line_stop list
        line_stops = []

        # loop over stops in line_dict
        for stop_name in line_dict["stops"]:

            # find stop by stop_name and add to line_stops
            stop = ssess.query(Stop).filter(Stop.name == stop_name).first()
            line_stops.append(stop)

        # predefine stops_order string
        stops_order = ""

        # loop over index and stop in line_stops
        for i, stop in enumerate(line_stops):

            # add stops into stops_order string (correct order)
            if i < len(line_stops) - 1:
                stops_order += f"{stop};"
            else:
                stops_order += f"{stop}"

        # add line_stops to stops attriute of line
        line.stops = line_stops

        # add stops_order to stops_order attribute of line
        line.stops_order = stops_order

        # update line to database
        ssess.add(line)
        ssess.commit()


def add_stops(dataset_name):
    """
    add all stops from <dataset_name>_stops csv-file to database

    parameters:
        dataset_name    - data files prefix;

    returns dict version of the stop class
        and has added the relationless version to the database
    """

    # get csv reader object from the datafile
    datafile_stops = open(f"../data/{dataset_name}_stops.csv", "r",
                          encoding="utf-8")
    stops_file = csv.reader(datafile_stops, delimiter=",")

    # skip headers
    next(stops_file)

    # predefine stops dictionary
    stops = dict()

    # loop over rows in stops_file
    for row in stops_file:

        # create dictionary for each unique line
        try:
            stops[row[0]]
        except KeyError:
            stops[row[0]] = dict()

        # add columns in row to corresponding keys
        stops[row[0]]["name"] = row[0]
        stops[row[0]]["stopnumber"] = row[2]
        stops[row[0]]["location"] = row[3]
        stops[row[0]]["stoptype"] = row[4]

        # predefine lines list for each unique stop
        try:
            stops[row[0]]["lines"]
        except KeyError:
            stops[row[0]]["lines"] = row[1].split(";")

    # loop over stop in stops (dict) and add stop to database
    for stop in stops.values():
        database_row = Stop(name=stop["name"], stopnumber=stop["stopnumber"],
                            location=stop["location"],
                            stoptype=stop["stoptype"])

        ssess.add(database_row)
        ssess.commit()

    return stops


def add_companies(dataset_name):
    """
    add all companies from <dataset_name>_companies csv-file to database

    parameters:
        dataset_name    - data files prefix;

    returns dict version of the company class
        and has added the relationless version to the database
    """

    # get csv reader object from the datafile
    datafile_companies = open(f"../data/{dataset_name}_companies.csv", "r",
                              encoding="utf-8")
    companies_file = csv.reader(datafile_companies, delimiter=",")

    # skip headers
    next(companies_file)

    # predefine companies dictionary
    companies = dict()

    # loop over rows in stops_file
    for row in companies_file:

        # create dictionary for each unique company
        try:
            companies[row[0]]
        except KeyError:
            companies[row[0]] = dict()

        # add columns in row to corresponding keys
        companies[row[0]]["name"] = row[0]
        companies[row[0]]["short_name"] = row[1]

        # predefine lines list for each unique company
        try:
            companies[row[0]]["lines"]
        except KeyError:
            companies[row[0]]["lines"] = []

        companies[row[0]]["lines"].append(row[2])

    # loop over company in companies (dict) and add company to database
    for company in companies.values():
        database_row = Company(name=company["name"],
                               short_name=company["short_name"])

        ssess.add(database_row)
        ssess.commit()

    return companies


def add_lines(dataset_name):
    """
    add all lines from <dataset_name>_lines csv-file to database

    parameters:
        dataset_name    - data files prefix;

    returns dict version of the line class
        and has added the relationless version to the database
    """

    # get csv reader object from the datafile
    datafile_lines = open(f"../data/{dataset_name}_lines.csv", "r",
                          encoding="utf-8")
    lines_file = csv.reader(datafile_lines, delimiter=",")

    # skip headers
    next(lines_file)

    # predefine lines dictionary
    lines = dict()

    # loop over rows in stops_file
    for row in lines_file:

        # create dictionary for each unique line
        try:
            lines[row[0]]
        except KeyError:
            lines[row[0]] = dict()

        # add columns in row to corresponding keys
        lines[row[0]]["name"] = row[0]
        lines[row[0]]["stopnumber_prefix"] = row[2]
        lines[row[0]]["stoptypes"] = row[3]
        lines[row[0]]["company"] = row[4]

        # predefine stops list for each unique line
        try:
            lines[row[0]]["stops"]
        except KeyError:
            lines[row[0]]["stops"] = []

        lines[row[0]]["stops"].append(row[1])

    # loop over line in lines (dict) and add line to database
    for line in lines.values():
        database_row = Line(name=line["name"],
                            stopnumber_prefix=line["stopnumber_prefix"],
                            stoptypes=line["stoptypes"])

        ssess.add(database_row)
        ssess.commit()

    return lines


# setup database engine, import models and run main if name is main
if __name__ == "__main__":

    # import models from app (get app from parent directory)
    #   https://stackoverflow.com/a/16985066
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

    # run main with arguments after filename
    main(sys.argv[1:])
