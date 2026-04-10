"""Production settings."""

from .base import *  # noqa: F401, F403
from .base import env

DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Whitenoise for static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
