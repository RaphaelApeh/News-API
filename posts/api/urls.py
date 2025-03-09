from django.urls import path

from rest_framework_simplejwt import views as jwt_view
from . import views

urlpatterns = [
    path("users/", views.UserRegisterView.as_view()),
    path("posts/", views.PostListView.as_view(), name="posts-list"),
    path("posts/<slug:slug>/", views.PostRetrieveView.as_view(), name="posts-detail"),
    path("users/posts/", views.UserPostsListView.as_view(), name="user-posts"),
    path("token/", views.TokenObtainView.as_view()),
    path("refresh/", jwt_view.TokenRefreshView.as_view())
]