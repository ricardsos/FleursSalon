from django.urls import path
from .views import venta_list, lineas_list, lineaServicio_create, lineaProducto_create, venta_delete, venta_edit, \
    venta_show, lineaServicio_delete

app_name = 'venta'

urlpatterns = [
    path('venta_list/', venta_list, name='venta_list'),
    path('venta_create/<int:id>/', lineas_list, name='venta_create'),
    path('venta_show/<int:id>/', venta_show, name='venta_show'),
    path('venta_edit/<int:id>/', venta_edit , name='venta_edit'),
    path('venta_delete/<int:id>/', venta_delete, name='venta_delete'),

    # Linea servicio
    path('lineaServicio_create/<int:id>/', lineaServicio_create, name='lineaServicio_create'),
    path('lineaServicio_delete/<int:id>/', lineaServicio_delete, name='lineaServicio_delete'),

    # Linea producto
    path('lineaProducto_create/<int:id>/', lineaProducto_create, name='lineaProducto_create'),

]

from __future__ import unicode_literals
from __future__ import absolute_import

from django.conf.urls import url, include
from .views import *

app_name = 'venta'

urlpatterns =[

    url(r'^facturar$', facturar, name="facturar"),
   
]