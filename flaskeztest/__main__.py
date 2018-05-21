"""Define functions which will be able to be ran through package."""

import sys
import os
import threading
from importlib import import_module

import eztestcase

USAGE_MESSAGE = "Usage: eztest flask_module \"test_module1, test_module2, ..., \" "


def flaskeztest_main(args=None):
    """
    Call this from main entry point of flaskeztest package.

    args: flask_module "test_module1, test_module2, ..., "
    """
    if args is None:
        try:
            args = sys.argv[1:]
        except IndexError:
            args = []

    if len(args) != 2:
        print USAGE_MESSAGE
        exit(1)

    flask_module = args[0]

    test_modules = [mod.trim() for mod in args[1].split(',')]

    flask_module = import_module(parse_module_name_from_filepath(flask_module))
    for mod in test_modules:
        import_module(parse_module_name_from_filepath(mod))

    app = flask_module.app
    eztest = flask_module.eztest

    eztest.run()

    app_thread = threading.Thread(target=run_app, args=(app, ))
    app_thread.setDaemon(True)  # exiting will also end this thread
    app_thread.start()


def parse_module_name_from_filepath(filepath):
    """
    Adds module file path to python path and returns the proper name that eztest should import.
    Most of this was taken from flask github source code
    :type filepath: str
    """
    path = os.path.realpath(filepath)

    if os.path.splitext(path)[1] == '.py':
        path = os.path.splitext(path)[0]

    if os.path.basename(path) == '__init__':
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, '__init__.py')):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return '.'.join(module_name[::-1])


if __name__ == '__main__':
    flaskeztest_main()
