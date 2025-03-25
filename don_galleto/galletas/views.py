from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.forms import ValidationError
from django.contrib import messages
from galletas.models import Galleta

# Create your views here.

class Lista_galletas_view(FormView):
    template_name = 'lista_galletas.html'
    
    def get_context_data(self):
        galletas = Galleta.objects.all()
        return {
            "galletas": galletas,
        }
        