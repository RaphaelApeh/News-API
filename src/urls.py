from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path("api/", include("posts.api.urls"))
]

if settings.DEBUG:
    urlpatterns.append(path("silk/", include("silk.urls")))