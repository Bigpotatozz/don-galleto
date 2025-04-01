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
from django.forms import ValidationError
from django.contrib import messages
from usuarios.utils import log

# Create your views here.

class Listado_insumos_view(PermissionRequiredMixin, FormView):
    
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
      
    template_name = 'lista_insumos.html'
    
    def get_context_data(self):
        verificar_insumos()
        insumos = Insumo.objects.all()
        return {
            "insumos": insumos,
        }

class Registrar_insumo_view(PermissionRequiredMixin, FormView):
    
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
      
    template_name = 'agregar_insumo.html'
    form_class = forms.Registro_insumo_form
    success_url = reverse_lazy('listado_insumos')
        
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):    
        log(self, form, "Error registro insumo")
        return super().form_invalid(form)
    
    
    
class Edicion_insumo_view(PermissionRequiredMixin, FormView):
    
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
      
    template_name = 'editar_insumo.html'
    form_class = forms.Edicion_insumo_form
    success_url = reverse_lazy('listado_insumos')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        insumo = get_object_or_404(Insumo, id_insumo = id)
        kwargs['instance'] = insumo
        return kwargs
    
    def form_valid(self, form):
        id = self.kwargs.get('id')
        form.save(id)
        return super().form_valid(form)
    
    def form_invalid(self, form):    
        log(self, form, "Error edicion insumo")
        return super().form_invalid(form)
    
class Registrar_compra_insumo_view(PermissionRequiredMixin, FormView):
    
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
      
    template_name = 'agregar_compra_insumo.html'
    form_class = forms.Registro_compra_insumo_form
    success_url = reverse_lazy('listado_insumos')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def form_invalid(self, form):    
        log(self, form, "Error registro compra insumo")
        return super().form_invalid(form)
    
class Registrar_merma_insumo_view(PermissionRequiredMixin, FormView):
    
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
      
    
    template_name = 'agregar_merma_insumo.html'
    form_class = forms.Registro_merma_insumo_form
    success_url = reverse_lazy('listado_insumos')
    
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request.user
        return kwargs
    
    
   
    
    def form_valid(self, form):
        
        try:
            form.save()
            return super().form_valid(form)
        except ValidationError as e:
            for error in e.messages:
                messages.error(self.request, error)
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Ocurrió un error: {str(e)}')
            return self.form_invalid(form)
            
        
    def form_invalid(self, form):    
        log(self, form, "Error registro merma insumo")
        return super().form_invalid(form)
    
   