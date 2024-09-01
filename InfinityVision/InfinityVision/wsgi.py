import os
import sys
from django.core.wsgi import get_wsgi_application

print(f"Current file path: {os.path.abspath(__file__)}")
print(f"sys.path before modification: {sys.path}")

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(f"sys.path after modification: {sys.path}")

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InfinityVision.settings')

# Get WSGI application
application = get_wsgi_application()
