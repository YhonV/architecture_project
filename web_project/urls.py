from django.urls import path, include
from web_project import views
from rest_framework import routers
from .api import ProductViewSet
from django.conf.urls.static import static
from django.conf import settings

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
    path("historial/", views.historial_compras, name="historial"),
    path("login/", views.user_login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("inventario/", views.inventario, name="inventario"),
    path("", include(router.urls)),
    path('logout/', views.exit , name= 'exit'),
     path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.mostrar_carrito, name='carrito'),
    path('eliminar_producto/', views.eliminar_producto, name='eliminar_producto'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('compra_exitosa/', views.compra_exitosa, name='compra_exitosa'),
   
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
