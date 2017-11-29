#!/usr/bin/env python
import os
import sys

python_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../../'
)
apps_path = os.path.join(
    os.path.realpath(os.path.dirname(__file__)), '../../'
)

# we add them first to avoid any collisions
sys.path.insert(0, python_path)
sys.path.insert(0, apps_path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
