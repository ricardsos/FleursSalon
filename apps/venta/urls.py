from __future__ import unicode_literals
from __future__ import absolute_import

from django.conf.urls import url, include
from .views import *

app_name = 'venta'

urlpatterns =[

    url(r'^facturar$', facturar, name="facturar"),
   
]