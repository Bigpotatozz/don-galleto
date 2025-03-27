from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import redirect,  get_object_or_404
from .models import Galleta, Detalle_receta
from .forms import GalletaForm, DetalleRecetaForm, GalletaEditarForm

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import Insumo, Detalle_receta, Galleta
from django.views.generic import DetailView
from . import forms

class ListaGalletasRecetaView(TemplateView):
    template_name = "lista_galletas_receta.html"
    def get_context_data(self):
        lista = Galleta.objects.all()
        return {
            "lista": lista
        }

class DetallesGalletaView(TemplateView):
    template_name = 'detalles_galleta_receta.html'
    def get_context_data(self, **kwargs):
        id = self.kwargs.get('id_galleta')
        galleta = Galleta.objects.get(id_galleta=id)

        return {
            'galleta': galleta
        }
    

class AgregarGalletaRecetaView(FormView):
    model = Galleta
    form_class = forms.GalletaForm
    template_name = "agregar_galleta_receta.html"
    success_url = reverse_lazy('seleccionar_insumos_receta')

    def form_valid(self, form):
        galleta = form.save()
        return redirect('seleccionar_insumos_receta', id_galleta=galleta.id_galleta)
    

class EditarGalletaRecetaView(FormView):
    template_name = "editar_galleta_receta.html"
    form_class = forms.GalletaEditarForm
    success_url = reverse_lazy('detalles_galleta_receta')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id_galleta = self.kwargs.get('id_galleta')
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        kwargs['instance'] = galleta
        return kwargs
    
    def form_valid(self, form):
        form.save(self.kwargs.get('id_galleta'))
        return redirect(reverse_lazy('editar_insumos_receta', kwargs={'id_galleta': self.kwargs.get('id_galleta')}))
        

class EditarInsumosRecetaView(TemplateView):
    template_name = "editar_insumos_receta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_galleta = self.kwargs.get('id_galleta')
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        insumos_receta = Detalle_receta.objects.filter(id_galleta=galleta)

        context['galleta'] = galleta
        context['insumos_receta'] = insumos_receta
        context['insumos'] = Insumo.objects.all()  
        return context
    
    def post(self, request, *args, **kwargs):
        id_galleta = self.kwargs.get('id_galleta')
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)

        for insumo in Insumo.objects.all():
            cantidad = request.POST.get(f'cantidad_{insumo.id_insumo}')

            if cantidad:
                cantidad = float(cantidad)
                Detalle_receta.objects.update_or_create(
                    id_galleta=galleta,
                    id_insumo=insumo,
                    defaults={'cantidad': cantidad}
                )

        return redirect(reverse_lazy('detalles_galleta_receta', kwargs={'id_galleta': id_galleta}))


class SeleccionarInsumosView(TemplateView):
    template_name = "seleccionar_insumos_receta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_galleta = self.kwargs.get('id_galleta')
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        insumos = Insumo.objects.all() 
        context['galleta'] = galleta
        context['insumos'] = insumos
        return context

    def post(self, request, *args, **kwargs):
        id_galleta = self.kwargs.get('id_galleta')
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        for insumo in Insumo.objects.all():
            cantidad = request.POST.get(f'cantidad_{insumo.id_insumo}')
            if f'insumo_{insumo.id_insumo}' in request.POST and cantidad:
                Detalle_receta.objects.create(id_galleta=galleta, id_insumo=insumo, cantidad=float(cantidad))
        return redirect('lista_galletas_receta')

