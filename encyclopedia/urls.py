from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("create", views.create, name="create")
    # path("<str:random>", views.random, name="random")
]
