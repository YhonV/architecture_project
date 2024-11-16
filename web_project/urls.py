from django.urls import path, include
from web_project import views
from rest_framework import routers
from .api import ProductViewSet

## Se crea un objeto de la clase DefaultRouter
## Esto nos permite crear una API RESTful, nos entrega una URL para cada vista
## Se registra la vista ProductViewSet
router = routers.DefaultRouter()
router.register('api/productos', ProductViewSet, 'productos')

urlpatterns = [
    path("", views.inicio, name="index"),
    path("contact/", views.contact, name="contact"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("perfil/", views.perfil, name="perfil"),
    path("historial/", views.historial, name="historial"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("inventario/", views.inventario, name="inventario"),
    path("", include(router.urls))
]