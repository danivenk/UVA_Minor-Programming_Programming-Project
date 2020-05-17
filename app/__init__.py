#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
version: python 3+
__init__.py imports all important modules in app
Dani van Enk, 11823526
"""

# used imports
import os
import sys

# import modules if name is package
if __name__ == "__package__":

    # https://stackoverflow.com/a/16985066
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    # import app modules
    import app.models
    import app.functions.search
    import app.functions.security
