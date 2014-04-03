#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    # Load the Heroku environment.
    from herokuapp.env import load_env
    load_env(__file__, "toolhub")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolhub.settings")
    # Add the lib/ directory to the system path
    sys.path.append("lib")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
