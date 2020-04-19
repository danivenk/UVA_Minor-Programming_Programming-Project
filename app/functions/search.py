#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
securiy.py defines the hash function and compare function
Dani van Enk, 11823526
"""

from itertools import combinations


def main():
    list_a = ["1", "2", "3"]

    print(relevance_query(list_a))


def relevance_query(in_list):

    for item in in_list:
        assert type(item) == str

    out_list = []

    for length in range(len(in_list) + 1):
        for subset in combinations(in_list, length):
            if len(subset) > 0:
                query = ""
                for item in list(subset):
                    query += f"{item} "

                out_list.append(query.strip())

    return out_list[::-1]


if __name__ == "__main__":
    main()
