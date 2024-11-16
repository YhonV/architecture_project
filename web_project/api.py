from .models import Producto
from rest_framework import viewsets, permissions
from .serializers import ProductoSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductoSerializer