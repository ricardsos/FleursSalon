
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
import datetime

# Create your views here.
def facturar(request):
    
    return render(request, 'venta/facturar.html')
