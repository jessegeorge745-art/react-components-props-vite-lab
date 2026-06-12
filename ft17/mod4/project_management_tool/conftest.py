# conftest.py
# Makes the project root importable for all tests.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))