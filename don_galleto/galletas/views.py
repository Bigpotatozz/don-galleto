from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.forms import ValidationError
from django.contrib import messages
from galletas.models import Galleta
from . import forms
from usuarios.utils import log
# Create your views here.

class Lista_galletas_view(PermissionRequiredMixin, FormView):
    permission_required = 'usuarios.empleado'
    
    
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = 'lista_galletas.html'
    
    
    def get_context_data(self):
        
        galletas = Galleta.objects.all().prefetch_related('detalle_receta_galleta__id_insumo')
        print(galletas)
        return {
            "galletas": galletas,
        }
        
        
class Registrar_galleta_view(PermissionRequiredMixin, FormView):
    
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
      
    
    template_name = 'agregar_galleta.html'
    form_class = forms.Registro_galleta_form
    success_url = reverse_lazy('listado_galletas')
    

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):   
        log(self, form, "Error registro galleta")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class Editar_galleta_view(PermissionRequiredMixin, FormView):
    permission_required = 'usuarios.empleado'
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = 'editar_galleta.html'
    form_class = forms.Editar_galleta_form
    success_url = reverse_lazy('listado_galletas')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        galleta = get_object_or_404(Galleta, id_galleta=id)
        kwargs['instance'] = galleta
        return kwargs


    def form_valid(self, form):
        id = self.kwargs.get('id')
        form.save(id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

