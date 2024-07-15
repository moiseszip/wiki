from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random_page, name="random"),
    path("<str:entry>", views.entry, name="entry")
]
