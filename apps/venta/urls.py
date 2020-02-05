from django.urls import path
from django.conf.urls import url, include
from .views import venta_list, lineas_list, lineaServicio_create, lineaProducto_create, venta_delete, venta_edit, \
    venta_show, lineaServicio_delete_edit, facturar, venta_list_delete, lineaServicio_create_edit, \
    lineaProducto_create_edit, lineaServicio_edit_edit, lineaProducto_delete_edit, lineaProducto_edit_edit, \
    lineaProducto_delete, lineaServicio_delete, lineaServicio_edit, lineaProducto_edit,saludar,venta_create,linea_venta_servicio

app_name = 'venta'

urlpatterns = [
    url(r'^facturar$', facturar, name="facturar"),
    path('saludar/<str:id>/<str:id2>/', saludar, name='saludar'),
    path('crearventa/<str:cliente>/<str:codigo>/<str:total>/', venta_create, name='venta_create'),
    path('linea_servicio/<str:id_venta>/<str:servicion>/<str:colaboradorn>/<str:precios>/<str:descripcion>/', linea_venta_servicio, name='linea_servicio'),
    path('venta_list/', venta_list, name='venta_list'),
    path('venta_create/<int:id>/', lineas_list, name='venta_create'),
    path('venta_show/<int:id>/', venta_show, name='venta_show'),
    path('venta_edit/<int:id>/', venta_edit , name='venta_edit'),
    path('venta_delete/<int:id>/', venta_delete, name='venta_delete'),
    path('venta_list_delete/<int:id>/', venta_list_delete, name='venta_list_delete'),

    # Linea servicio
    path('lineaServicio_create/<int:id>/', lineaServicio_create, name='lineaServicio_create'),
    path('lineaServicio_edit/<int:id>/', lineaServicio_edit, name='lineaServicio_edit'),
    path('lineaServicio_delete/<int:id>/', lineaServicio_delete, name='lineaServicio_delete'),

    # Retorna a editar venta
    path('lineaServicio_create_edit/<int:id>/', lineaServicio_create_edit, name='lineaServicio_create_edit'),
    path('lineaServicio_edit_edit/<int:id>/', lineaServicio_edit_edit, name='lineaServicio_edit_edit'),
    path('lineaServicio_delete_edit/<int:id>/', lineaServicio_delete_edit, name='lineaServicio_delete_edit'),

    # Linea producto
    path('lineaProducto_create/<int:id>/', lineaProducto_create, name='lineaProducto_create'),
    path('lineaProducto_edit/<int:id>/', lineaProducto_edit, name='lineaProducto_edit'),
    path('lineaProducto_delete/<int:id>/', lineaProducto_delete, name='lineaProducto_delete'),

    # Retorna a editar venta
    path('lineaProducto_create_edit/<int:id>/', lineaProducto_create_edit, name='lineaProducto_create_edit'),
    path('lineaProducto_edit_edit/<int:id>/', lineaProducto_edit_edit, name='lineaProducto_edit_edit'),
    path('lineaProducto_delete_edit/<int:id>/', lineaProducto_delete_edit, name='lineaProducto_delete_edit'),

]



