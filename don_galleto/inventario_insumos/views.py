from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout
from inventario_insumos.models import Insumo

# Create your views here.

class Listado_insumos_view(FormView):
    template_name = 'lista_insumos.html'
    
    def get_context_data(self):
        insumos = Insumo.objects.all()
        
        return {
            "insumos": insumos,
        }
        