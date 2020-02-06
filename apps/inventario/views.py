from django.shortcuts import render, redirect
from apps.inventario.models import Producto, Servicio
from django.contrib.auth.decorators import login_required

def prueba(request):
    return render(request, 'inventario/agregarInventario.html')

def prueba2(request):
    return render(request, 'inventario/listInventario.html')