import os
import sys

if __name__ == "__package__":
    # https://stackoverflow.com/a/16985066
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    import app.models
    import app.functions.search
    import app.functions.security
