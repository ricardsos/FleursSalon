from django.shortcuts import render, redirect
from .models import Venta, Servicio, Colaborador, LineaDeServicio, LineaDeProducto, Producto
from datetime import datetime, date

from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
from decimal import Decimal


# Create your views here.

def saludar(request,id,id2):
	print(id)
	print(id2)
	return HttpResponse('')


def facturar(request):
	products =  Producto.objects.all()
	services = Servicio.objects.all()
	colabo = Colaborador.objects.all()
	return render(request, 'venta/facturar.html', context={'products': products,'services':services,'colabo':colabo})


#FUNCIONES

# Funcion para obtener el codigo de la venta
def obtenerCodigo(idVenta):
	fecha = date.today()
	if fecha.day <= 9:
		if fecha.month <= 9:
			codigo = f'{0}{fecha.day}{0}{fecha.month}{fecha.year}{idVenta}'
		else:
			codigo = f'{0}{fecha.day}{fecha.month}{fecha.year}{idVenta}'
	else:
		if fecha.month <= 9:
			codigo = f'{fecha.day}{0}{fecha.month}{fecha.year}{idVenta}'
		else:
			codigo = f'{fecha.day}{fecha.month}{fecha.year}{idVenta}'
	print(codigo)
	return codigo

# VENTAS


# Listar ventas GUARDADAS y se crea una Venta con datos por defecto
def venta_create(request,cliente,codigo,total):
	venta = Venta()
	venta.cliente = cliente
	venta.codigo = 0
	venta.fecha = date.today()
	venta.total = total
	venta.anulado = True
	venta.estado = 'N'
	venta.save()
	id = venta.id
	print(id)
	return HttpResponse(id)
def linea_venta_servicio(request,id_venta,servicion,colaboradorn,precios,descripcion):
	lineaServicio = LineaDeServicio()
	venta = Venta.objects.get(id=id_venta)
	lineaServicio.venta = venta
	print(servicion)
	servicio = Servicio.objects.get(nombre=servicion)
	lineaServicio.servicio = servicio
	colaborador = Colaborador.objects.get(username=colaboradorn)
	lineaServicio.colaborador = colaborador
	lineaServicio.precio = Decimal('0.0')
	lineaServicio.descuento = 0  # request.POST.get('descuento')
	lineaServicio.nuevoPrecio = Decimal(precios)
	lineaServicio.descripcion = descripcion
	lineaServicio.save()
	return HttpResponse('')

def linea_venta_producto(request,id_venta,producton,cantidad,nuevoprecio,sbtotal):
	lineaProducto = LineaDeProducto()
	venta = Venta.objects.get(id=id_venta)
	lineaProducto.venta = venta
	producto = Producto.objects.get(nombre=producton)
	lineaProducto.producto = producto
	lineaProducto.cantidad = cantidad
	lineaProducto.descuento = 0  # request.POST.get('descuento')
	lineaProducto.nuevoPrecio = nuevoprecio
	lineaProducto.subtotal = sbtotal
	lineaProducto.save()
	return HttpResponse('')


def venta_list(request):
	# ventas = Venta.objects.all()
	ventas = Venta.objects.filter(estado='G')

	if request.method == 'POST':
		venta = Venta()
		venta.cliente = 'CLIENTE SIN ASIGNAR'
		venta.codigo = 0
		venta.fecha = date.today()
		venta.total = 0.0
		venta.anulado = True
		venta.estado = 'N'
		venta.save()
		id = venta.id
		return redirect('venta:venta_create', id=id)
	return render(request, template_name='venta/venta_list.html', context={'ventas': ventas})


# En caso de haber hecho una nueva venta, y haber cancelado se elimina la nueva venta creada con datos por defecto
def venta_list_delete(request, id):
	venta = Venta.objects.get(id=id)
	venta.delete()
	print('venta_list_delete')
	return redirect('venta:venta_list')
	return render(request, template_name='venta/venta_create.html', context={'id': id})


def venta_show(request, id):
	venta = Venta.objects.get(id=id)
	lineasServicio = LineaDeServicio.objects.filter(venta__id=id)
	lineasProducto = LineaDeProducto.objects.filter(venta__id=id)
	#print(venta.total)
	return render(request, template_name='venta/venta_show.html', context={'venta': venta,
																			'lineasServicio': lineasServicio,
																			'lineasProducto': lineasProducto})


def venta_edit(request, id):
	venta = Venta.objects.get(id=id)
	lineasServicio = LineaDeServicio.objects.filter(venta__id=id)
	lineasProducto = LineaDeProducto.objects.filter(venta__id=id)
	if request.method == 'POST':
		venta.cliente = request.POST.get('cliente')
		venta.save()
		return redirect('venta:venta_list')
	return render(request, template_name='venta/venta_edit.html', context={'venta': venta,
																			'lineasServicio': lineasServicio,
																			'lineasProducto': lineasProducto})


def venta_delete(request, id):
	venta = Venta.objects.get(id=id)
	lineasServicio = LineaDeServicio.objects.filter(venta__id=id)
	lineasProducto = LineaDeProducto.objects.filter(venta__id=id)

	if request.method == 'POST':
		venta.delete()
		return redirect('venta:venta_list')
	return render(request, template_name='venta/venta_delete.html', context={'venta': venta,
																				'lineasServicio': lineasServicio,
																				'lineasProducto': lineasProducto})


def lineas_list(request, id):
	lineasServicio = LineaDeServicio.objects.filter(venta__id=id)
	lineasProducto = LineaDeProducto.objects.filter(venta__id=id)

	codigo = obtenerCodigo(id)
	venta = Venta.objects.get(id=id)
	total = 0
	if request.method == 'POST':
		venta.cliente = request.POST.get('cliente')
		venta.codigo = codigo  # Codigo generado por el sistema
		venta.fecha = date.today()
		venta.anulado = False
		venta.estado = 'G'
		venta.save()
		return redirect('venta:venta_list')

	# Actualizar el total del la venta
	for lineaServicio in lineasServicio:
		total += lineaServicio.nuevoPrecio
	for lineaProducto in lineasProducto:
		total += lineaProducto.nuevoPrecio
	venta.total = total
	venta.save()
	return render(request, template_name='venta/venta_create.html', context={'venta': venta, 'codigo': codigo,
																					'lineasServicio': lineasServicio,
																					'lineasProducto': lineasProducto})


def lineaServicio_create(request, id):
	servicios = Servicio.objects.all()
	colaboradores = Colaborador.objects.all()
	venta = Venta.objects.get(id=id)
	if request.method == 'POST':
		lineaServicio = LineaDeServicio()

		venta = Venta.objects.get(id=id)
		lineaServicio.venta = venta

		servicio = Servicio.objects.get(nombre=request.POST.get('servicio'))
		lineaServicio.servicio = servicio

		colaborador = Colaborador.objects.get(id=request.POST.get('colaborador'))
		lineaServicio.colaborador = colaborador

		lineaServicio.precio = request.POST.get('precio')
		lineaServicio.descuento = 0  # request.POST.get('descuento')
		lineaServicio.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaServicio.descripcion = request.POST.get('descripcion')
		lineaServicio.save()
		return redirect('venta:venta_create', id=id)
	return render(request, template_name='venta/lineaServicio_create.html', context={'servicios': servicios,
																					'venta': venta,
																					'colaboradores': colaboradores,})


def lineaServicio_edit(request, id):
	lineaServicio = LineaDeServicio.objects.get(id=id)
	venta = Venta.objects.get(id=lineaServicio.venta.id)
	servicios = Servicio.objects.all()
	colaboradores = Colaborador.objects.all()
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		# venta = Venta.objects.get(id=id)
		# lineaServicio.venta = venta

		servicio = Servicio.objects.get(nombre=request.POST.get('servicio'))
		lineaServicio.servicio = servicio

		colaborador = Colaborador.objects.get(last_name=request.POST.get('colaborador'))
		lineaServicio.colaborador = colaborador

		lineaServicio.precio = request.POST.get('precio')
		lineaServicio.descuento = 0  # request.POST.get('descuento')
		lineaServicio.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaServicio.descripcion = request.POST.get('descripcion')
		lineaServicio.save()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=venta.id)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=venta.id)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		print('Funciona edit')
		return redirect('venta:venta_create', id=venta.id)
	return render(request, template_name='venta/lineaServicio_edit.html', context={'venta': venta,
																					'lineaServicio': lineaServicio,
																					'servicios': servicios,
																					'colaboradores': colaboradores})


def lineaServicio_delete(request, id):
	lineaServicio = LineaDeServicio.objects.get(id=id)
	venta = Venta.objects.get(id=lineaServicio.venta.id)
	idventa = venta.id
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaServicio.delete()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=idventa)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=idventa)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_create', id=idventa)
	return render(request, template_name='venta/lineaServicio_delete.html', context={'lineaServicio': lineaServicio,
																					'venta': venta})


# Crea una linea de servicio y redirecciona a editar venta
def lineaServicio_create_edit(request, id):
	servicios = Servicio.objects.all()
	colaboradores = Colaborador.objects.all()
	venta = Venta.objects.get(id=id)
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaServicio = LineaDeServicio()

		venta = Venta.objects.get(id=id)
		lineaServicio.venta = venta

		servicio = Servicio.objects.get(nombre=request.POST.get('servicio'))
		lineaServicio.servicio = servicio

		colaborador = Colaborador.objects.get(last_name=request.POST.get('colaborador'))
		lineaServicio.colaborador = colaborador

		lineaServicio.precio = request.POST.get('precio')
		lineaServicio.descuento = request.POST.get('descuento')
		lineaServicio.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaServicio.descripcion = request.POST.get('descripcion')
		lineaServicio.save()
		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=id)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=id)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		print('Funciona')
		return redirect('venta:venta_edit', id=id)
	return render(request, template_name='venta/lineaServicio_create_edit.html', context={'servicios': servicios,
																					'venta': venta,
																					'colaboradores': colaboradores})


def lineaServicio_edit_edit(request, id):
	lineaServicio = LineaDeServicio.objects.get(id=id)
	venta = Venta.objects.get(id=lineaServicio.venta.id)
	servicios = Servicio.objects.all()
	colaboradores = Colaborador.objects.all()
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		#venta = Venta.objects.get(id=id)
		#lineaServicio.venta = venta

		servicio = Servicio.objects.get(nombre=request.POST.get('servicio'))
		lineaServicio.servicio = servicio

		colaborador = Colaborador.objects.get(last_name=request.POST.get('colaborador'))
		lineaServicio.colaborador = colaborador

		lineaServicio.precio = request.POST.get('precio')
		lineaServicio.descuento = request.POST.get('descuento')
		lineaServicio.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaServicio.descripcion = request.POST.get('descripcion')
		lineaServicio.save()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=venta.id)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=venta.id)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		print('Funciona edit')
		return redirect('venta:venta_edit', id=venta.id)
	return  render(request, template_name='venta/lineaServicio_edit_edit.html', context={'venta': venta,
																					'lineaServicio': lineaServicio,
																					'servicios': servicios,
																					'colaboradores': colaboradores})


def lineaServicio_delete_edit(request, id):
	lineaServicio = LineaDeServicio.objects.get(id=id)
	venta = Venta.objects.get(id=lineaServicio.venta.id)
	idventa = venta.id
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaServicio.delete()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=idventa)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=idventa)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_edit', id=idventa)
	return render(request, template_name='venta/lineaServicio_delete_edit.html', context={'lineaServicio': lineaServicio,
																					'venta': venta})


# PRODUCTO
def lineaProducto_create(request, id):
	productos = Producto.objects.all()
	if request.method == 'POST':
		lineaProducto = LineaDeProducto()

		venta = Venta.objects.get(id=id)
		lineaProducto.venta = venta

		producto = Producto.objects.get(nombre=request.POST.get('producto'))
		lineaProducto.producto = producto

		lineaProducto.cantidad = request.POST.get('cantidad')
		lineaProducto.descuento = 0  # request.POST.get('descuento')
		lineaProducto.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaProducto.subtotal = request.POST.get('subtotal')
		lineaProducto.save()
		return redirect('venta:venta_create', id=id)
	return render(request, template_name='venta/lineaProducto_create.html', context={'id': id,'productos': productos})


def lineaProducto_delete(request, id):
	lineaProducto = LineaDeProducto.objects.get(id=id)
	venta = Venta.objects.get(id=lineaProducto.venta.id)
	idventa = venta.id
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaProducto.delete()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=idventa)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=idventa)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_create', id=idventa)
	return render(request, template_name='venta/lineaProducto_delete.html', context={'lineaProducto': lineaProducto,
																					'venta': venta})


def lineaProducto_edit(request, id):
	lineaProducto = LineaDeProducto.objects.get(id=id)
	venta = Venta.objects.get(id=lineaProducto.venta.id)
	productos = Producto.objects.all()
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaProducto.venta = venta

		producto = Producto.objects.get(id=request.POST.get('producto'))
		lineaProducto.producto = producto

		lineaProducto.cantidad = request.POST.get('cantidad')
		lineaProducto.descuento = 0  # request.POST.get('descuento')
		lineaProducto.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaProducto.subtotal = request.POST.get('subtotal')
		lineaProducto.save()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=venta.id)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=venta.id)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_create', id=venta.id)
	return render(request, template_name='venta/lineaProducto_edit.html', context={'venta': venta,
																					'lineaProducto': lineaProducto,
																					'productos': productos})


# Crea una linea de producto y redirecciona a editar venta
def lineaProducto_create_edit(request, id):
	productos = Producto.objects.all()
	venta = Venta.objects.get(id=id)
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaProducto = LineaDeProducto()
		lineaProducto.venta = venta

		producto = Producto.objects.get(id=request.POST.get('producto'))
		lineaProducto.producto = producto

		lineaProducto.cantidad = request.POST.get('cantidad')
		lineaProducto.descuento = request.POST.get('descuento')
		lineaProducto.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaProducto.subtotal = request.POST.get('subtotal')
		lineaProducto.save()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=id)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=id)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_edit', id=id)
	return render(request, template_name='venta/lineaProducto_create_edit.html', context={'venta': venta,
																						'productos': productos})


def lineaProducto_edit_edit(request, id):
	lineaProducto = LineaDeProducto.objects.get(id=id)
	venta = Venta.objects.get(id=lineaProducto.venta.id)
	productos = Producto.objects.all()
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaProducto.venta = venta

		producto = Producto.objects.get(id=request.POST.get('producto'))
		lineaProducto.producto = producto

		lineaProducto.cantidad = request.POST.get('cantidad')
		lineaProducto.descuento = request.POST.get('descuento')
		lineaProducto.nuevoPrecio = request.POST.get('nuevoprecio')
		lineaProducto.subtotal = request.POST.get('subtotal')
		lineaProducto.save()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=venta.id)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=venta.id)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_edit', id=venta.id)
	return render(request, template_name='venta/lineaProducto_edit_edit.html', context={'venta': venta,
																					'lineaProducto': lineaProducto,
																					'productos': productos})


def lineaProducto_delete_edit(request, id):
	lineaProducto = LineaDeProducto.objects.get(id=id)
	venta = Venta.objects.get(id=lineaProducto.venta.id)
	idventa = venta.id
	totalServicio = 0
	totalProducto = 0
	if request.method == 'POST':
		lineaProducto.delete()

		# Actualizar el total del la venta
		lineasServicio = LineaDeServicio.objects.filter(venta__id=idventa)
		LineasProducto = LineaDeProducto.objects.filter(venta__id=idventa)

		for lineaServicio in lineasServicio:
			totalServicio += lineaServicio.nuevoPrecio

		for LineaProducto in LineasProducto:
			totalProducto += LineaProducto.nuevoPrecio

		venta.total = totalServicio + totalProducto
		venta.save()
		return redirect('venta:venta_edit', id=idventa)
	return render(request, template_name='venta/lineaProducto_delete_edit.html', context={'lineaProducto': lineaProducto,
																					'venta': venta})
