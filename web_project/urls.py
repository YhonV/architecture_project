from django.urls import path
from web_project import views

urlpatterns = [
    path("", views.inicio, name="index"),
    path("contact/", views.contact, name="contact"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("perfil/", views.perfil, name="perfil"),
    path("historial/", views.historial, name="historial"),
    path("login/", views.login, name="login"),
]