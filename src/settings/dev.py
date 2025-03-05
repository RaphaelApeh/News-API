from .base import * # NOQA

INSTALLED_APPS.extend(["silk"])

MIDDLEWARE.extend(["silk.middleware.SilkyMiddleware"])

CORS_ALLOW_ALL_ORIGINS = True
