from django.urls import path

from . import views

urlpatterns = [
    path('v1/', views.list_posts_view, name="list-posts")
]