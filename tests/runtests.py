#!/usr/bin/env python

import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

import pytest  # noqa


if __name__ == "__main__":
    sys.exit(pytest.main())
