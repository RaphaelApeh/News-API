from django.urls import path

from rest_framework_simplejwt import views as jwt_view
from . import views

urlpatterns = [
    path("posts/", views.PostListView.as_view()),
    path("token/", jwt_view.TokenObtainPairView.as_view()),
    path("refresh/", jwt_view.TokenRefreshView.as_view())
]