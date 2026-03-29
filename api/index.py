import os
import sys

# Make the backend package importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from api.main import app  # noqa: E402
