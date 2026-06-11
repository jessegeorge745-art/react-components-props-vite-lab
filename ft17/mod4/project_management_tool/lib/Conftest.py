# conftest.py
# Adds the project root to sys.path so all module imports resolve correctly
# regardless of which directory pytest is invoked from.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))