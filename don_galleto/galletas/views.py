from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from galletas.models import Galleta, Detalle_receta

# Create your views here.
class ListaGalletasRecetaView(TemplateView):
    template_name = "lista_galletas_receta.html"
    
    def get_context_data(self):
        lista = Galleta.objects.all()
        return {
            "lista": lista
        }