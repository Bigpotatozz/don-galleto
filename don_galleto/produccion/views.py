from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from . import forms
from django.views import View  
from django.utils.timezone import now
from produccion.models import Lote_galleta, Galleta, Merma_producto
from usuarios.models import Usuario
from django.urls import reverse_lazy
from .forms import MermaRegistrarForm

# Create your views here.}
class ListaGalletasView(TemplateView):
    template_name = "lista_galletas_solicitud.html"
    def get_context_data(self):
        lista = Galleta.objects.all()
        return {
            "lista": lista
        }


class CrearLoteView(View):
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        lote = Lote_galleta.objects.create(
            cantidad_galletas=galleta.cantidad,
            id_galleta=galleta,
            id_usuario=Usuario.objects.get(id_usuario=1), 
            estatus='Pendiente',
            fecha_preparacion=now()
        )
        return redirect('lista_produccion')
    
class ListaProduccionView(TemplateView):
    template_name = "lista_produccion.html"
    def get_context_data(self):
        lista = Lote_galleta.objects.all()
        return {
            "lista": lista
        }
        

class CambiarEstatusLote(View):
    def post(self, request, id_lote_galleta):
        lote = get_object_or_404(Lote_galleta, id_lote_galleta=id_lote_galleta)
        nuevo_estatus = request.POST.get('estatus')
        lote.estatus = nuevo_estatus
        lote.save()
        return redirect('lista_produccion')
    


class AgregarMermaView(FormView):
    template_name = "crear_merma.html"
    form_class = MermaRegistrarForm
    success_url = reverse_lazy('lista_produccion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_lote = self.kwargs.get('id_lote_galleta')
        lote = get_object_or_404(Lote_galleta, id_lote_galleta=id_lote)
        context['lote'] = lote
        return context

    def form_valid(self, form):
        lote = get_object_or_404(Lote_galleta, id_lote_galleta=self.kwargs['id_lote_galleta'])
        merma = form.save(commit=False)
        merma.id_lote_galleta = lote
        merma.save()
        return super().form_valid(form)
