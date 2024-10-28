from django.urls import path
from web_project import views

urlpatterns = [
    path("", views.inicio, name="index"),
]