from django.urls import path
from .views import (
    register,
    logout_view,
    login_view,
    subscribe,
    unfollow_user,
    list_of_follow,
)

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("unfollow/<int:followed_user_id>/", unfollow_user, name="unfollow_user"),
    path("followers/", list_of_follow, name="followers"),
    path("subscriptions/", subscribe, name="subscriptions"),
]
