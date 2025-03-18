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
        