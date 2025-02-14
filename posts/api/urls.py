from django.urls import path

from rest_framework_simplejwt import views as jwt_view
from . import views

urlpatterns = [
    path("posts/", views.PostListView.as_view()),
    path("posts/<slug:slug>/", views.PostRetrieveView.as_view(), name="posts-detail"),
    path("token/", jwt_view.TokenObtainPairView.as_view()),
    path("refresh/", jwt_view.TokenRefreshView.as_view())
]