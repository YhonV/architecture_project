from django.db import models
import uuid

# Create your models here.
class Cliente (models.Model):
    id_cliente = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_completo