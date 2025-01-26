from .base import *

INSTALLED_APPS.extend(["silk"])

MIDDLEWARE.extend(["silk.middleware.SilkyMiddleware"])