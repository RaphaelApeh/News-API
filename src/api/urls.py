from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # Auth token
    path('token/', obtain_auth_token),

    # version one
    path('v1/news/', views.list_posts_view, name="list-posts"),
    
    path('v1/news/<slug:slug>/', views.detail_post_view, name="post-detail"), 
    
    path('v1/create/', views.create_post_view, name="post-create"),

    path('likes/<slug:slug>', views.user_post_like_view, name='user-likes'),

    # Class Base View
    path('register/', views.UserRegistrationView.as_view()),
    path('users/', views.UsersPostView.as_view()),
]