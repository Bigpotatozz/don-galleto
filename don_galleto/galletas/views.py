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
        galletas = Galleta.objects.all()
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
