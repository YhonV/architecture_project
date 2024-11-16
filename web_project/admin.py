from django.contrib import admin
from web_project.models import Producto
# Register your models here.
# De esta forma podemos registrar los modelos en el administrador de Django
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    pass