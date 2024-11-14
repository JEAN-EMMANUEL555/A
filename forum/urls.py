from django.urls import path
from .views import (
    home,
    login_view,
    register_view,
    feed,
    create_post,
    add_comment,
    like_post,
    user_profile,
    search_view
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # URL d'authentification
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', home, name='home'),
    path('feed/', feed, name='feed'),
    path('post/new/', create_post, name='create_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('search/', search_view, name='search_results'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
