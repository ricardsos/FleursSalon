from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Producto(models.Model):
	nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
	precio = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, blank=False, null=False)
	estado = models.BooleanField()
	activo = models.BooleanField()

	def __str__(self):
		return ' {}, PRECIO: ${}'.format(self.nombre, self.precio)

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'


class Servicio(models.Model):
	nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
	activo = models.BooleanField()

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'Servicio'
		verbose_name_plural = 'Servicios'


class Stock(models.Model):
	producto = models.ForeignKey(Producto, null=False, on_delete=models.PROTECT, blank=False)
	cantidad = models.IntegerField('Cantidad', blank=False, null=False, validators=[MinValueValidator(0)])

	def __str__(self):
		return ' {}, STOCK: {}'.format(self.producto.nombre, self.cantidad)

	class Meta:
		verbose_name = 'Stock'
		verbose_name_plural = 'Stock'


class Compra(models.Model):
	producto = models.ForeignKey(Producto, null=False, on_delete=models.PROTECT, blank=False)
	fecha = models.DateField('Fecha', blank=False, null=False)
	cantidad = models.IntegerField('Cantidad', blank=False, null=False, validators=[MinValueValidator(0)])

	def __str__(self):
		return 'Dia: {}, PRODUCTO: {}'.format(self.fecha, self.producto.nombre)

	class Meta:
		verbose_name = 'Compra'
		verbose_name_plural = 'Compras'