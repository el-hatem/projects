"""The Url page."""
from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.rondomize_pages, name="random"),
    path("serach/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("save/", views.save, name="save"),
    path("add/", views.add_post, name="add_post")
]
