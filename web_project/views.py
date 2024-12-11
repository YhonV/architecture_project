from gettext import translation
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.shortcuts import get_object_or_404, redirect, render
import json
from django.contrib.auth.models import User
from web_project.forms import RegistroForm
from django.http import JsonResponse
from .models import Cliente, Compra, DetalleCompra, Producto, TipoProducto
from django.utils.timezone import now


# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})

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

def user_login(request):
    if request.method == 'POST':
        usuario = request.POST.get('email')
        password = request.POST.get('password')

        print(request.POST)

        if not usuario:
            return JsonResponse({'status': 'error', 'message': 'Debe ingresar un nombre de usuario'}, status=400)

        if not password:
            return JsonResponse({'status': 'error', 'message': 'Debe ingresar la contraseña'}, status=400)

        user = authenticate(request, username=usuario, password=password)
        if user is None:
            return JsonResponse({'status': 'error', 'message': 'Usuario o contraseña incorrecto'}, status=400)
        else:
            auth_login(request, user)
            return JsonResponse({'status': 'success', 'redirect': reverse('index')})

    return render(request,'registration/login.html')

def exit(request):
    logout(request)
    return redirect('index')

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


def agregar_al_carrito(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            id_producto = data.get("id_producto")

            # Buscar el producto por su UUID
            producto = Producto.objects.get(id_producto=id_producto)

            # Lógica para agregar al carrito (usando sesión como ejemplo)
            carrito = request.session.get("carrito", {})
            if str(id_producto) in carrito:
                carrito[str(id_producto)]["cantidad"] += 1
            else:
                carrito[str(id_producto)] = {
                    "nombre": producto.nombre_producto,
                    "precio": producto.precio_unitario,
                    "cantidad": 1
                }
            
            request.session["carrito"] = carrito  # Guardar carrito en sesión
            
            return JsonResponse({"success": True, "mensaje": "Producto agregado al carrito"})
        except Producto.DoesNotExist:
            return JsonResponse({"success": False, "mensaje": "Producto no encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "mensaje": str(e)}, status=500)
    return JsonResponse({"success": False, "mensaje": "Método no permitido"}, status=405)

def format_to_chilean_pesos(value):
    return f"{value:,.0f}".replace(",", ".")

def mostrar_carrito(request):
    carrito = request.session.get("carrito", {})
    carrito_total = 0  # Variable para almacenar el total del carrito

    # Calcular el total por producto y el total del carrito
    for id_producto, detalles in carrito.items():
        producto = get_object_or_404(Producto, id_producto=id_producto)  # Recupera el producto de la base de datos
        detalles['imagen_url'] = producto.imagen.url if producto.imagen else '/static/images/default.jpg'
        detalles['total_por_producto'] = detalles['precio'] * detalles['cantidad']  # Calculamos el total por producto
        carrito_total += detalles['total_por_producto']  # Sumamos al total del carrito

    # Calcular IVA y total con IVA
    iva = carrito_total * 0.19  # El 19% del total neto
    carrito_total_iva = carrito_total + iva  # Total incluyendo IVA

    # Formatear los valores
    carrito_total_formateado = format_to_chilean_pesos(carrito_total)
    iva_formateado = format_to_chilean_pesos(iva)
    carrito_total_iva_formateado = format_to_chilean_pesos(carrito_total_iva)

    # Formatear los totales por producto
    for detalles in carrito.values():
        detalles['precio_formateado'] = format_to_chilean_pesos(detalles['precio'])  # Formateamos el precio
        detalles['total_por_producto_formateado'] = format_to_chilean_pesos(detalles['total_por_producto'])  # Formateamos el total por producto

    return render(
        request, 
        "carrito.html", 
        {
            "carrito": carrito, 
            "carrito_total": carrito_total_formateado,
            "iva": iva_formateado,
            "carrito_total_iva": carrito_total_iva_formateado,
        }
    )



def eliminar_producto(request):
    if request.method == "POST":
        try:
            # Intentar leer el cuerpo de la solicitud
            data = json.loads(request.body)
            id_producto = data.get('id_producto')

            # Validar si `id_producto` está presente
            if not id_producto:
                return JsonResponse({'success': False, 'mensaje': 'ID de producto no proporcionado'})

            # Lógica para eliminar el producto del carrito
            carrito = request.session.get('carrito', {})
            if id_producto in carrito:
                del carrito[id_producto]
                request.session['carrito'] = carrito
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'mensaje': 'Producto no encontrado en el carrito'})
        except json.JSONDecodeError as e:
            # Manejar errores de análisis JSON
            return JsonResponse({'success': False, 'mensaje': 'Error al procesar la solicitud: cuerpo mal formado'})
        except Exception as e:
            return JsonResponse({'success': False, 'mensaje': str(e)})
    return JsonResponse({'success': False, 'mensaje': 'Método no permitido'})

def finalizar_compra(request):
    # Verificar si el cliente está autenticado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para finalizar la compra.")
        return redirect('login')

    # Obtener el cliente asociado al usuario
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, "No se encontró información del cliente.")
        return redirect('carrito')

    # Obtener el carrito desde la sesión
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "El carrito está vacío.")
        return redirect('carrito')

    # Crear el DetalleCompra
    valor_total = sum(detalles['precio'] * detalles['cantidad'] for detalles in carrito.values())
    detalle_compra = DetalleCompra.objects.create(
        cliente=cliente,
        fecha=now().date(),
        valor_total=valor_total,
    )

    # Crear cada Compra relacionada
    for id_producto, detalles in carrito.items():
        try:
            producto = Producto.objects.get(id_producto=id_producto)
            cantidad = detalles['cantidad']
            precio_unitario = detalles['precio']
            valor_neto = precio_unitario * cantidad
            valor_iva = valor_neto * 0.19

            Compra.objects.create(
                detalle_compra=detalle_compra,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                valor_neto=valor_neto,
                valor_iva=valor_iva,
            )
        except Producto.DoesNotExist:
            messages.error(request, f"El producto con ID {id_producto} no existe.")
            continue

    # Vaciar el carrito
    request.session['carrito'] = {}
    messages.success(request, "Compra realizada con éxito.")
    return redirect('compra_exitosa')

def compra_exitosa(request):
    return render(request, 'compra.html')

