from django.contrib import admin
from django.urls import path
from ventas.views import dashboard_ventas
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('dashboard_generales/', dashboard_ventas, name='dashboard_ventas'),
]
