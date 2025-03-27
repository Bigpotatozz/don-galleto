from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout
from usuarios.models import Usuario, Logs
from usuarios.utils import asignar_permisos
from datetime import date



class Lista_usuarios_view(PermissionRequiredMixin, TemplateView):
    
    permission_required = 'usuarios.admin'
    template_name = 'lista_usuarios.html'
    def handle_no_permission(self):
        return redirect('home')
    
    
    def get_context_data(self):
        usuarios = Usuario.objects.all()
        
        return {
            "usuarios": usuarios
        }
        

class Registro_admin_view(PermissionRequiredMixin,FormView):
  
    permission_required = 'usuarios.admin'

    def handle_no_permission(self):
        return redirect('home')
    
    template_name = 'agregar_usuario.html'
    form_class = forms.Registro_admin_form
    success_url = reverse_lazy('listado_usuarios')
    
    
    def form_valid(self, form):
        
        asignar_permisos(form, None)
        
        if self.request.user.is_authenticated:
            Logs.objects.create(
                fecha = date.today(),
                tipo = "registro usuario",
                descripcion = "registro de usuario",
                id_usuario = self.request.user
            )
        
        return super().form_valid(form)

    def form_invalid(self, form):
        
        if self.request.user.is_authenticated:
            Logs.objects.create(
                fecha = date.today(),
                tipo = "error registro usuario",
                descripcion = "error registro de usuario",
                id_usuario = self.request.user
            )
        return super().form_invalid(form)
    
    
    
    
class Edicion_usuario_view(FormView):
    
    permission_required = 'usuarios.admin'

    def handle_no_permission(self):
        return redirect('home')
    
    template_name = 'editar_usuario.html'
    form_class = forms.Edicion_usuario_form
    success_url = reverse_lazy('listado_usuarios')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        usuario = get_object_or_404(Usuario, id_usuario=id)
        kwargs['instance'] = usuario
        return kwargs

    def form_valid(self, form):
        id = self.kwargs.get('id')
        asignar_permisos(form, id) 
        return super().form_valid(form)


def eliminar_usuario(request, id):
        
    usuario = get_object_or_404(Usuario, id_usuario=id)
    usuario.is_active = False
    usuario.save()
    return redirect('listado_usuarios')