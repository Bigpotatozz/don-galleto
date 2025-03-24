from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout
from inventario_insumos.models import Insumo
from inventario_insumos.utils import verificar_insumos

# Create your views here.

class Listado_insumos_view(FormView):
    template_name = 'lista_insumos.html'
    
    def get_context_data(self):
        verificar_insumos()
        insumos = Insumo.objects.all()
        return {
            "insumos": insumos,
        }

class Registrar_insumo_view(FormView):
    template_name = 'agregar_insumo.html'
    form_class = forms.Registro_insumo_form
    success_url = reverse_lazy('listado_insumos')
        
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class Registrar_compra_insumo_view(FormView):
    template_name = 'agregar_compra_insumo.html'
    form_class = forms.Registro_compra_insumo_form
    success_url = reverse_lazy('listado_insumos')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)