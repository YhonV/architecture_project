from django.db import models
from django.contrib.auth.models import User
import uuid

# Modelo Cliente
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id_cliente = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

# Modelo DetalleCompra
class DetalleCompra(models.Model):
    id_detalle_compra = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    valor_total = models.FloatField()


    def __str__(self):
        return f"DetalleCompra {self.id_detalle_compra}"

# Modelo Compra
class Compra(models.Model):
    id_compra = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detalle_compra = models.ForeignKey(DetalleCompra, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.FloatField()
    valor_neto = models.FloatField()
    valor_iva = models.FloatField()

    def __str__(self):
        return f"Compra {self.id_compra}"

# Modelo Producto
class Producto(models.Model):
    id_producto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_producto = models.CharField(max_length=100)
    desc_producto = models.CharField(max_length=100)
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE)
    precio_unitario = models.FloatField()
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True)

    def __str__(self):
        return self.nombre_producto

# Modelo TipoProducto
class TipoProducto(models.Model):
    id_tipo_producto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_tipo_producto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo_producto

# Modelo Administrador
class Administrador(models.Model):
    id_administrador = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

# Modelo ComentarioValoracion
class ComentarioValoracion(models.Model):
    id_comentario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=300)
    valoracion = models.IntegerField()
    fecha = models.DateField()

    def __str__(self):
        return f"Comentario {self.id_comentario}"

# Modelo ReporteVenta
class ReporteVenta(models.Model):
    id_reporte = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_reporte = models.CharField(max_length=100)
    fecha_reporte = models.DateField()
    total_ventas = models.IntegerField()
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reporte {self.id_reporte}"

# Modelo Respaldo
class Respaldo(models.Model):
    id_respaldo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_respaldo = models.DateField()
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return f"Respaldo {self.id_respaldo}"

# Modelo MedioPago
class MedioPago(models.Model):
    id_medio_pago = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_medio_pago = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_medio_pago
