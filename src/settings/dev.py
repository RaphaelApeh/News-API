from .base import * # NOQA

INSTALLED_APPS.extend(["silk"])

MIDDLEWARE.extend(["silk.middleware.SilkyMiddleware"])