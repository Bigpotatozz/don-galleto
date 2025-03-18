from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout
from usuarios.models import Usuario



    
class Lista_usuarios_view(TemplateView):
    template_name = 'lista_usuarios.html'
    
    def get_context_data(self):
        usuarios = Usuario.objects.all()
        
        return {
            "usuarios": usuarios
        }
        
class Editar_usuario_view(FormView):
    template_name = 'editar_usuario.html'
    form_class = forms.Form_editar_usuario
    success_url = reverse_lazy('listado_usuarios')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.kwargs.get('id')
        usuario = get_object_or_404(Usuario, id_usuario = id)
        kwargs['instance'] = usuario
        return kwargs
    
    def form_valid(self, form):
        form.save(self.kwargs.get('id'))
        return super().form_valid(form)