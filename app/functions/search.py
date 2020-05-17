#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
search.py defines the relevance_query and macron_query functions
Dani van Enk, 11823526
"""

# used import
from itertools import combinations


def main():
    """
    main function to test if the functions in this module work
    """

    # define test list a
    list_a = ["1", "2", "3"]

    # print result of the relevance_query
    print(relevance_query(list_a))

    # define test text b
    b = "Osaka-ku"

    # print result of the macron_query
    print(macron_query(b))


def relevance_query(in_list):
    """
    relevance_query searches for all lengths of subqueries

    parameter:
        in_list     - list of query words;
        out_list    - list of queries from full query to subqueries;

    returns a list of queries from full query and its subqueries sorted by
        number of query words (large to small)
    """

    # make sure all items in in_list are string
    for item in in_list:
        assert type(item) == str

    # predefine out_list
    out_list = []

    # loop over the all possible lengths of subsets of in_list
    for length in range(len(in_list) + 1):

        # loop over all subsets of in_list
        for subset in combinations(in_list, length):

            if len(subset) > 0:
                query = ""

                # add all items in the subset to a string
                for item in list(subset):
                    query += f"{item} "

                # add the string to the out_list
                out_list.append(query.strip())

    # reverse items to have larger to smaller strings
    return out_list[::-1]


def macron_query(query):
    """
    macron_query returns all possible queries with vowels replaced with
        it's macron partner

    parameter:
        query   - query string;

    return a list with all possible queries where the vowels are replaced
        with it's macron partner
    """

    # define all vowels with it's macron partner
    accents = {"A": "Ā", "a": "ā", "I": "Ī", "i": "ī", "U": "Ū",
               "u": "ū", "E": "Ē", "e": "ē", "O": "Ō", "o": "ō"}

    # predefine a vowel list for the query
    vowels = []

    # find all vowels in the query
    for i, letter in enumerate(query):
        if letter in accents:
            vowels.append((letter, i))

    # predefine the queries set with the query
    queries = {query}

    # loop over all possible lengths of the vowels subset
    for length in range(len(vowels) + 1):

        # loop over all possible subsets of the vowels
        for subset in combinations(vowels, length):
            if len(subset) > 0:
                query = list(query)

                # replace all vowels from the subset with macron counterpart
                for letter in subset:
                    query[letter[1]] = accents[letter[0]]

                query = "".join(query)

                # add query to queries set
                queries.add(query)

    return queries


# run main if name is main
if __name__ == "__main__":
    main()
