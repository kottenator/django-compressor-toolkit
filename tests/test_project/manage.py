#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

    from tests.conftest import pytest_configure
    from django.core.management import execute_from_command_line

    pytest_configure()
    execute_from_command_line(sys.argv)
