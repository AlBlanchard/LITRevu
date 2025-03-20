from django.urls import path
from .views import flux, self_posts

urlpatterns = [
    path("", flux, name="home"),
    path("posts/", self_posts, name="self_posts"),
]
