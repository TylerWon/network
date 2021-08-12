
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes
    path("posts", views.posts, name="posts"),
    path("posts/user/<str:username>", views.user_posts, name="user_posts"),
    path("posts/user/<str:username>/following", views.user_following_posts, name="user_following_posts"),
    path("posts/<int:post_id>/update", views.update_post, name="update_post"),
    path("<str:username>", views.user, name="user"),
]
