from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def navbar(request):
    return render(request, 'navbar.html')

def contact(request):
    return render(request, 'contact.html')