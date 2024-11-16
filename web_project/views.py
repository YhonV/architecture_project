from django.shortcuts import render
from .models import Producto, TipoProducto
from web_project.forms import RegistroForm
from django.http import JsonResponse

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def catalogo(request):
    return render(request, 'catalogo.html')

def perfil(request):
    return render(request, 'perfil.html')

def historial(request):
    return render(request, 'historial-compra.html')

def login(request):
    return render(request, 'login.html')

def registro(request):
    form = RegistroForm()
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir después del registro
    return render(request, "registro.html", {"form": form})

def inventario(request):
    
    #Metodo para crear productos
    #Extraer datos del formulario
    #Realizamos unos controles para verificar que los datos sean correctos
    #Creamos el objeto producto y lo guardamos en la base de datos
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nombre_categoria = request.POST.get('nombre_categoria')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        imagen = request.FILES.get('imagen')

        if Producto.objects.filter(nombre_producto=nombre).exists():
            return JsonResponse({"success": False, "message": "No puedes agregar un producto cuyo nombre ya exista."})

        try:
            stock = int(stock)
        except ValueError:
            return JsonResponse({"success": False, "message": "Stock debe ser un número entero positivo."})

        try:
            precio = float(precio)
        except ValueError:
            return JsonResponse({"success": False, "message": "Precio debe ser un número positivo."})

        categoria_objeto = TipoProducto.objects.get(nombre_tipo_producto=nombre_categoria)
        producto = Producto(
            nombre_producto=nombre,
            desc_producto=descripcion,
            tipo_producto=categoria_objeto,
            precio_unitario=precio,
            stock=stock,
            imagen=imagen
        )
        if producto.precio_unitario < 0:
            return JsonResponse({"success": False, "message": "Precio no puede ser negativo."})
        
        if producto.stock < 0:
            return JsonResponse({"success": False, "message": "Stock no puede ser negativo."})
        producto.save()
        return JsonResponse({"success": True, "message": "Producto creado correctamente."})
    
    productos = Producto.objects.all()
    contexto = {'productos': productos, 'categorias': TipoProducto.objects.all()}
    return render(request, 'inventario.html', contexto)

