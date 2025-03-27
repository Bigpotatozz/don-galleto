from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from . import forms
from django.views import View  
from django.utils.timezone import now
from produccion.models import Lote_galleta, Merma_producto
from galletas.models import Galleta, Detalle_receta
from inventario_insumos.models import Insumo
from usuarios.models import Usuario
from django.urls import reverse_lazy
from .forms import MermaRegistrarForm
from django.db import transaction
from django.contrib import messages

# Create your views here.
#Obtener la lista de galletas para crear los lotes
class ListaGalletasView(TemplateView):
    template_name = "lista_galletas_solicitud.html"
    def get_context_data(self):
        lista = Galleta.objects.all()
        return {
            "lista": lista
        }


#Creación de lotes, descontando insumos del inventario
class CrearLoteView(View):
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        
        # Verificación de insumos disponibles
        insumos_inventario = []
        for detalle_receta in galleta.detalle_receta_galleta.all():
            if detalle_receta.id_insumo.cantidad < detalle_receta.cantidad:
                insumos_inventario.append(detalle_receta.id_insumo.nombre)
                print(f"Falta insumo: {detalle_receta.id_insumo.nombre} (Necesario: {detalle_receta.cantidad}")
        
        if insumos_inventario:
            print(f"No se puede producir lote de {galleta.nombre}. Insumos faltantes: {', '.join(insumos_inventario)}") #Por ahora solo es para debugear
            return redirect('lista_galletas_solicitud')
        
        # Creación del lote, pero aún no sumamos al stock, porque primero se debe de ir actualizando el estatus hasta llegar a completado
        print(f"Creando lote de {galleta.cantidad_receta} galletas de {galleta.nombre}")
        lote = Lote_galleta.objects.create(
            cantidad_galletas=galleta.cantidad_receta,
            id_galleta=galleta,
            id_usuario=Usuario.objects.get(id_usuario=1),
            estatus='Pendiente',
            fecha_preparacion=now()
        )
        
        # Descontamos los insumos utilizados para la galleta
        print("Descontando insumos:")
        for detalle_receta in galleta.detalle_receta_galleta.all():
            insumo = detalle_receta.id_insumo
            print(f"Insumos a descontar: - {insumo.nombre}: {insumo.cantidad} -> {insumo.cantidad - detalle_receta.cantidad}")
            insumo.cantidad -= detalle_receta.cantidad
            insumo.save()
            
        return redirect('lista_produccion')
    
#Lista de todos los lotes de produccion
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
        
        if nuevo_estatus == 'Completado':
            # Calcular total de mermas, por ejemplo si en un lote se hacen 50 galletas y se me tiraron 10, las que debe de agregar a la cantidad de galleta son 40 
            mermas = Merma_producto.objects.filter(id_lote_galleta=lote)
            total_mermas_galleta = 0
            for merma_producto in mermas:
                total_mermas_galleta += merma_producto.cantidad
            
            galletas_disponibles = lote.cantidad_galletas - total_mermas_galleta
            
            # Actualizar stock de las galletas 
            galleta = lote.id_galleta
            galleta.cantidad += galletas_disponibles
            galleta.save()
            
            print(f"Lote completado. Galletas añadidas al stock: {galletas_disponibles}")

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
        
        print(f"Merma registrada: {merma.cantidad} galletas del lote {lote.id_lote_galleta}")
        return super().form_valid(form)