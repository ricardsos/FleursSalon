from django.shortcuts import render, redirect
from .models import Venta, Servicio, Colaborador, LineaDeServicio, LineaDeProducto, Producto
from datetime import datetime, date

from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json


# Create your views here.

def facturar(request):
	return render(request, 'venta/facturar.html')

# VENTAS


# Listar ventas GUARDADAS y se crea una Venta con datos por defecto
def venta_list(request):
	#ventas = Venta.objects.all()
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

	venta = Venta.objects.get(id=id)
	total = 0
	if request.method == 'POST':
		venta.cliente = request.POST.get('cliente')
		venta.codigo = request.POST.get('codigo')  # Codigo generado por el sistema
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
	return render(request, template_name='venta/venta_create.html', context={'venta': venta,
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

		colaborador = Colaborador.objects.get(last_name=request.POST.get('colaborador'))
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
def lineaServicio_create_edit(request, id):
	servicios = Servicio.objects.all()
	colaboradores = Colaborador.objects.all()
	venta = Venta.objects.get(id=id)
	total = 0
	if request.method == 'POST':
		lineaServicio = LineaDeServicio()

		venta = Venta.objects.get(id=id)
		lineaServicio.venta = venta

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
		lineasServicio = LineaDeServicio.objects.filter(venta__id=id)

		for lineaServicio in lineasServicio:
			total += lineaServicio.nuevoPrecio
		venta.total = total
		venta.save()
		print('Funciona')
		return redirect('venta:venta_edit', id=id)
	return render(request, template_name='venta/lineaServicio_create_edit.html', context={'servicios': servicios,
																					 'venta': venta,
																					 'colaboradores': colaboradores,})

def lineaServicio_edit(request, id):

	return  render(request, template_name='venta/lineaServicio_create.html', context={})


def lineaServicio_delete(request, id):
	lineaServicio = LineaDeServicio.objects.get(id=id)
	venta = Venta.objects.get(id=lineaServicio.venta.id)
	idventa = venta.id

	if request.method == 'POST':
		lineaServicio.delete()
		return redirect('venta:venta_edit', id=idventa)
	#print(id)
	#lineaServicio.delete()
	return render(request, template_name='venta/lineaServicio_delete.html', context={'lineaServicio': lineaServicio,
																					 'idventa': idventa})


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