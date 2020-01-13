from django.db import models
from django.core.validators import MinValueValidator
from apps.inventario.models import Producto, Servicio
from apps.usuario.models import Colaborador
# Create your models here.


class Venta(models.Model):
	colaborador = models.ForeignKey(Colaborador, null=False, on_delete=models.CASCADE, blank=False)
	cliente = models.CharField('Cliente', max_length=100, blank=False, null=False)
	codigo = models.IntegerField('Código', max_length=9, blank=False, null=False)
	fecha = models.DateField('Fecha', blank=False, null=False)
	total = models.DecimalField('TOTAL', max_digits=5, decimal_places=2, blank=True, null=False, validators =
			[MinValueValidator(0)], default=0)
	anulado = models.BooleanField()

	def __str__(self):
		return 'Dia: {}, Colaborador: {}, {}'.format(self.fecha, self.colaborador.last_name, self.colaborador.first_name)

	class Meta:
		verbose_name = 'Venta'
		verbose_name_plural = 'Ventas'

class LineaDeProducto(models.Model):
	# Borrar On_delete
	venta = models.ForeignKey(Venta, null=False, on_delete=models.CASCADE, blank=False)
	producto = models.OneToOneField(Producto, null=False, on_delete=models.CASCADE, blank=False)
	cantidad = models.IntegerField('Cantidad', blank=False, null=False, validators=[MinValueValidator(1)])
	descuento = models.IntegerField('Descuento (%)', blank=False, null=False, validators=[MinValueValidator(0)])
	nuevoPrecio = models.DecimalField('Nuevo precio', max_digits=5, decimal_places=2, blank=False, null=False)
	subtotal = models.DecimalField('Subtotal', max_digits=5, decimal_places=2, blank=False, null=False)

	def __str__(self):
		return 'CÓDIGO VENTA: {},  Producto: {}'.format(self.venta.codigo, self.producto.nombre)

	class Meta:
		verbose_name = 'Linea de producto'
		verbose_name_plural = 'Lineas de producto'


class LineaDeServicio(models.Model):
	# Borrar On_delete
	venta = models.ForeignKey(Venta, null=False, on_delete=models.CASCADE, blank=False)
	servicio = models.OneToOneField(Servicio, null=False, on_delete=models.CASCADE, blank=False)
	precio = models.DecimalField('Precio unitario', max_digits=5, decimal_places=2, blank=False, null=False)
	descuento = models.IntegerField('Descuento (%)', blank=False, null=False, validators=[MinValueValidator(0)])
	nuevoPrecio = models.DecimalField('Nuevo precio', max_digits=5, decimal_places=2, blank=False, null=False)
	descripcion = models.CharField('Descripcion', max_length=300, blank=False, null=False)

	def __str__(self):
		return 'CÓDIGO VENTA: {},  Servicio: {}'.format(self.venta.codigo, self.servicio.nombre)

	class Meta:
		verbose_name = 'Linea de servicio'
		verbose_name_plural = 'Lineas de servicio'
