from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from proovedores.models import Proovedor
from . import forms
from django.urls import reverse_lazy

# Create your views here.
class CrearProovedorView(FormView):
    template_name = "crear_proovedor.html"  
    form_class = forms.ProovedorRegistrarForm
    success_url = reverse_lazy("crear_proovedor")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ListaProovedorView(TemplateView):
    template_name = "lista_proovedores.html"
    def get_context_data(self):
        lista = Proovedor.objects.all()
        return {"lista": lista}