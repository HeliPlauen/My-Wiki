from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.chosen, name="chosen"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),    
    path("edit", views.edit, name="edit")
]

