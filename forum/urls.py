from django.urls import path
from .views import (
    home,
    thread_list,
    thread_detail,
    create_thread,
    add_post,
    add_comment,
    user_profile,
    follow_user,
    unfollow_user,
    toggle_like,
    login_view,
    register_view
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # URL d'authentification
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    # URL des threads
    path('', home, name='home'),
    path('threads/', thread_list, name='thread_list'),
    path('thread/create/', create_thread, name='create_thread'),
    path('thread/<int:thread_id>/', thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/add_post/', add_post, name='add_post'),
    # URL des posts et des commentaires
    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', toggle_like, name='toggle_like'),
    # URL des utilisateurs
    path('user/<int:user_id>/', user_profile, name='user_profile'),
    path('user/<int:user_id>/follow/', follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', unfollow_user, name='unfollow_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]