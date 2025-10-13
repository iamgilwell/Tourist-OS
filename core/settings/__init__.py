"""
Settings package for the Tourist Management System.

Import the appropriate settings module based on DJANGO_SETTINGS_MODULE environment variable.
Default to development settings if not specified.
"""

import os

# Determine which settings to use
ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "staging":
    from .staging import *
elif ENVIRONMENT == "testing":
    from .testing import *
else:
    from .development import *

# Print current environment (useful for debugging)
print(f"🚀 Django running in {ENVIRONMENT.upper()} mode")
