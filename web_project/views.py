from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
import json
from django.contrib.auth.models import User


from web_project.forms import RegistroForm
from django.http import JsonResponse
from .models import Producto, TipoProducto
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

def registro(request):
    form = RegistroForm()

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get('email')
            pass1 = form.cleaned_data.get('password')
            pass2 = form.cleaned_data.get('password2')
            nombre = form.cleaned_data.get('nombre')

            if pass1 == pass2:
                if User.objects.filter(username=usuario).exists():
                    response = {
                        'status': 'error',
                        'message': 'El usuario ya está registrado!'
                    }
                else:
                    user = User.objects.create_user(username=usuario, 
                                                    email=usuario, 
                                                    password=pass1,
                                                    first_name=nombre,)
                    user.save()
                    response = {
                        'status': 'success',
                        'message': 'Registro exitoso!',
                        'redirect': reverse('login')
                    }
                    return JsonResponse(response)
            else:
                response = {
                    'status': 'error',
                    'message': 'Las contraseñas deben coincidir'
                }
        else:
            response = {
                'status': 'error',
                'message': 'Formulario inválido'
            }
        return JsonResponse(response)

    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('email')
        password = request.POST.get('password')

        if not usuario:
            return JsonResponse({'status': 'error', 'message': 'Debe ingresar un nombre de usuario'}, status=400)

        if not password:
            return JsonResponse({'status': 'error', 'message': 'Debe ingresar la contraseña'}, status=400)

        user = authenticate(request, username=usuario, password=password)
        if user is None:
            return JsonResponse({'status': 'error', 'message': 'Usuario o contraseña incorrecto'}, status=400)
        else:
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect': reverse('inicio')})

    return render(request,'registration/login.html')



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
    
    if request.method == 'DELETE':
        print("Cuerpo de la solicitud:", request.body)
        body = json.loads(request.body)
        id_producto = body.get('id_producto')
        producto = Producto.objects.get(id_producto=id_producto)
        producto.delete()
        return JsonResponse({"success": True, "message": "Producto eliminado correctamente."})
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        print("Cuerpo de la solicitud:", request.body)
        id_producto = data.get('id_producto')
        nombre_producto = data.get('nombre_producto')
        tipo_producto_nombre = data.get('tipo_producto')
        precio_unitario = data.get('precio_unitario')
        stock = data.get('stock')
        
        if not all([id_producto, nombre_producto, tipo_producto_nombre, precio_unitario, stock]):
            return JsonResponse({"success": False, "message": "No puede haber campos vacíos."})
        
        try:
            stock = int(stock)
        except ValueError:
            return JsonResponse({"success": False, "message": "Stock debe ser un número entero."})
        
        try:
            precio_unitario = float(precio_unitario)
        except ValueError:
            return JsonResponse({"success": False, "message": "Precio debe ser un número positivo."}) 
        
        try:
            producto = Producto.objects.get(id_producto=id_producto)
            tipo_producto = TipoProducto.objects.get(nombre_tipo_producto=tipo_producto_nombre)
            producto.nombre_producto = nombre_producto
            producto.tipo_producto = tipo_producto
            producto.precio_unitario = precio_unitario
            if producto.precio_unitario < 0:
                return JsonResponse({"success": False, "message": "Precio no puede ser negativo."})
            producto.stock = stock
            if producto.stock < 0:
                return JsonResponse({"success": False, "message": "Stock no puede ser negativo."})
            producto.save()
            return JsonResponse({"success": True, "message": "Producto actualizado correctamente."})
        except Producto.DoesNotExist:
            return JsonResponse({"success": False, "message": "Producto no encontrado."})
        except TipoProducto.DoesNotExist:
            return JsonResponse({"success": False, "message": "Categoría no encontrada."})
    
    productos = Producto.objects.all()
    contexto = {'productos': productos, 'categorias': TipoProducto.objects.all()}
    return render(request, 'inventario.html', contexto)