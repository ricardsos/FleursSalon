from django.contrib import admin
from .models import Producto, Compra, Servicio, Stock
# Register your models here.

admin.site.register(Compra)
admin.site.register(Producto)
admin.site.register(Servicio)
admin.site.register(Stock)

