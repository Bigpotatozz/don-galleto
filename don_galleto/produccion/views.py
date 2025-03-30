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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = Galleta.objects.all()
        

        for galleta in lista:
            if galleta.cantidad < 100: 
                messages.warning(self.request, f"Debes preparar más galletas de la {galleta.nombre}")
                
            galleta.ultimo_lote_galleta = Lote_galleta.objects.filter(
                id_galleta=galleta
            ).order_by('-id_lote_galleta').first()

        context["lista"] = lista
        return context


    
#Lista de todos los lotes de produccion
class ListaProduccionView(TemplateView):
    template_name = "lista_produccion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["lista"] = Lote_galleta.objects.exclude(estatus="Completado")
        return context
        


    
class CrearLoteView(View):
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        
        #Verificar si hay sufiente stock
        if galleta.cantidad >= 100: 
            messages.error(request, f"Ya hay suficiente stock ({galleta.cantidad} galletas), no se puede crear otro lote.")
            return redirect('lista_galletas_solicitud')
        
        #Verificar si la galleta tiene insumos
        if not galleta.detalle_receta_galleta.exists():
            messages.error(request, "Esta receta no tiene insumos.")
            return redirect('lista_galletas_solicitud')
        
        #Verificar si hay suficientes insumos para la preparación de la galleta
        insumos_faltantes = []
        for detalle_receta in galleta.detalle_receta_galleta.all():
            if detalle_receta.id_insumo.cantidad < detalle_receta.cantidad:
                insumos_faltantes.append(f"{detalle_receta.id_insumo.nombre} (Faltante: {detalle_receta.cantidad - detalle_receta.id_insumo.cantidad})")
        
        
        if insumos_faltantes:
            messages.error(request, f"Insumos insuficientes: {', '.join(insumos_faltantes)}")
            return redirect('lista_galletas_solicitud')
        
        #Crear im lote nuevo de galletas
        lote = Lote_galleta.objects.create(
            cantidad_galletas=galleta.cantidad_por_lote,
            id_galleta=galleta,
            id_usuario=Usuario.objects.get(id_usuario=1),
            estatus='Pendiente',
            fecha_preparacion=now()
        )
        
        #Descontamos insumos de la galleta 
        for detalle_receta in galleta.detalle_receta_galleta.all():
            insumo = detalle_receta.id_insumo
            insumo.cantidad -= detalle_receta.cantidad
            insumo.save()

        messages.success(request, f"Lote de {galleta.cantidad_por_lote} galletas creado correctamente. Para la galleta {galleta.nombre}")
        
        return redirect('lista_produccion')


class CambiarEstatusLote(View):
    def post(self, request, id_lote_galleta):
        lote = get_object_or_404(Lote_galleta, id_lote_galleta=id_lote_galleta)
        nuevo_estatus = request.POST.get('estatus')
        
        lote.estatus = nuevo_estatus
        lote.save()
        
        if nuevo_estatus == 'Completado':
            mermas = Merma_producto.objects.filter(id_lote_galleta=lote)
            total_mermas_galleta = 0
            for merma_producto in mermas:
                total_mermas_galleta += merma_producto.cantidad
            
            galletas_disponibles = lote.cantidad_galletas - total_mermas_galleta
            
            #Actualizamos stock disponible de galletas despues de agregar la merma
            galleta = lote.id_galleta
            galleta.cantidad += galletas_disponibles
            galleta.save()
            
            messages.success(request, f"Lote {lote.id_lote_galleta} completado. Galletas añadidas al stock: {galletas_disponibles}")

        lote.estatus = nuevo_estatus
        lote.save()
        return redirect('lista_produccion')

class AgregarMermaView(FormView):
    template_name = "crear_merma.html"
    form_class = MermaRegistrarForm
    success_url = reverse_lazy('lista_produccion')

    def form_valid(self, form):
        lote = get_object_or_404(Lote_galleta, id_lote_galleta=self.kwargs['id_lote_galleta'])
        merma = form.save(commit=False)
        merma.id_lote_galleta = lote
        merma.save()
        
        messages.success(self.request, f"Merma registrada: {merma.cantidad} galletas del lote {lote.id_lote_galleta}")
        return super().form_valid(form)