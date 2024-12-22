from django.urls import path

from . import views

urlpatterns = [
    path('v1/', views.list_posts_view, name="list-posts"),
    
    path('v1/news/<slug:slug>/', views.detail_post_view, name="post-detail"), 
    
    path('v1/create/', views.create_post_view, name="post-create")
]