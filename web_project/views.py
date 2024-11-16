from django.shortcuts import render

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
    return render(request, 'registro.html')

def inventario(request):
    return render(request, 'inventario.html')


#Crear un producto en el inventario.html
def crear_producto(request):
    return render(request, 'crear-producto.html')