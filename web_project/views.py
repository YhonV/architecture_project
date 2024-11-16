from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.urls import reverse

from web_project.forms import RegistroForm

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

def registro(request):
    form = RegistroForm()
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir después del registro
    return render(request, "registro.html", {"form": form})

def inventario(request):
    return render(request, 'inventario.html')


#Crear un producto en el inventario.html
def crear_producto(request):
    return render(request, 'crear-producto.html')
