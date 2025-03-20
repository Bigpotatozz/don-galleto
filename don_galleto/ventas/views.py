from django.shortcuts import render
from ventas.models import Venta
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from . import forms

class Lista_Ventas_View(TemplateView):
    template_name = 'lista_ventas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ventas'] = Venta.objects.all()
        return context
    



