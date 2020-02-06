from django.urls import path
from django.conf.urls import url, include
from apps.inventario.views import prueba, prueba2

app_name = 'inventario'

urlpatterns = [
    path('inventarioAgregar/', prueba, name='prueba'),
    path('inventarioList/', prueba2, name='prueba2'),
]