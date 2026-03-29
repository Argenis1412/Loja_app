import os
import sys

# Add the 'backend' folder to sys.path
# This ensures that when we do 'from api.main import app', 
# Python can find the 'api' package inside the 'backend' folder.
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_path)

# Import the app and rename it to 'app' for Vercel
try:
    from api.main import app as fastapi_app
    app = fastapi_app
except ImportError as e:
    # This helps debug if the path manipulation fails in Vercel
    print(f"ImportError in api/index.py: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Backend path expected at: {backend_path}")
    raise e
