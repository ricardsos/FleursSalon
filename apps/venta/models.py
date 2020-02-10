from django.db import models
from django.core.validators import MinValueValidator
from apps.inventario.models import Producto, Servicio
from apps.usuario.models import Colaborador
# Create your models here.


class Venta(models.Model):
	NOGUARDADA = 'N'
	GUARDADA = 'G'
	ESTADO_CHOICES = (
		(NOGUARDADA, 'No guardada'),
		(GUARDADA, 'Guardada'),
	)

	cliente = models.CharField('Cliente', max_length=100, blank=False, null=False)
	email = models.CharField('E-mail', max_length=50, blank=False, null=False)
	telefono = models.IntegerField('Teléfono', blank=False, null=False)
	codigo = models.CharField('Código',max_length=100, blank=False, null=False)
	fecha = models.DateField('Fecha', blank=False, null=False)
	subtotal = models.DecimalField('Subtotal', max_digits=5, decimal_places=2, blank=True, null=False, validators =
			[MinValueValidator(0)], default=0)  # No incluye IVA
	total = models.DecimalField('TOTAL', max_digits=5, decimal_places=2, blank=True, null=False, validators =
			[MinValueValidator(0)], default=0)  # Incluye IVA
	anulado = models.BooleanField()
	estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default=None, blank=False, null=False)

	def __str__(self):
		return 'Dia: {}, Código: {}, Estado: {}'.format(self.fecha, self.codigo, self.estado)

	class Meta:
		verbose_name = 'Venta'
		verbose_name_plural = 'Ventas'


class LineaDeProducto(models.Model):
	# Borrar On_delete
	venta = models.ForeignKey(Venta, null=False, on_delete=models.CASCADE, blank=False)
	producto = models.ForeignKey(Producto, null=False, on_delete=models.CASCADE, blank=False)
	cantidad = models.IntegerField('Cantidad', blank=False, null=False, validators=[MinValueValidator(1)])
	colaborador = models.ForeignKey(Colaborador, null=False, on_delete=models.CASCADE, blank=False)
	descuento = models.IntegerField('Descuento (%)', blank=False, null=False, validators=[MinValueValidator(0)])
	subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, blank=False, null=False)
	nuevoSubtotal = models.DecimalField('Nuevo subtotal', max_digits=10, decimal_places=2, blank=False, null=False)

	def __str__(self):
		return 'CÓDIGO VENTA: {},  Producto: {}'.format(self.venta.codigo, self.producto.nombre)

	class Meta:
		verbose_name = 'Linea de producto'
		verbose_name_plural = 'Lineas de producto'


class LineaDeServicio(models.Model):
	# Borrar On_delete
	venta = models.ForeignKey(Venta, null=False, on_delete=models.CASCADE, blank=False)
	servicio = models.ForeignKey(Servicio, null=False, on_delete=models.CASCADE, blank=False)
	colaborador = models.ForeignKey(Colaborador, null=False, on_delete=models.CASCADE, blank=False)
	precio = models.DecimalField('Precio', max_digits=10, decimal_places=2, blank=False, null=False)
	descuento = models.IntegerField('Descuento (%)', blank=False, null=False, validators=[MinValueValidator(0)])
	nuevoPrecio = models.DecimalField('Nuevo precio', max_digits=5, decimal_places=2, blank=False, null=False)
	descripcion = models.CharField('Descripcion', max_length=300, blank=False, null=False)

	def __str__(self):
		return 'CÓDIGO VENTA: {},  Servicio: {}'.format(self.venta.codigo, self.servicio.nombre)

	class Meta:
		verbose_name = 'Linea de servicio'
		verbose_name_plural = 'Lineas de servicio'
