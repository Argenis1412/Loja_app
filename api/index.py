import os
import sys

# Get the absolute path to the backend directory
# 'api' is at root, 'backend' is at root level too.
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))

# Add backend directory to sys.path to allow imports from api, domain, etc.
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Import the FastAPI app from backend/api/main.py
try:
    from api.main import app
except ImportError as e:
    print(f"Error importing app: {e}")
    print(f"sys.path: {sys.path}")
    raise e

# Vercel's python runtime will look for an 'app' instance
# exported as a variable.
handler = app
