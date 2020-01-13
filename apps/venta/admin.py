from django.contrib import admin
from .models import Venta, LineaDeProducto, LineaDeServicio
# Register your models here.

admin.site.register(Venta)
admin.site.register(LineaDeProducto)
admin.site.register(LineaDeServicio)

