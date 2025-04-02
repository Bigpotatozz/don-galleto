from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView, View
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib import messages
from produccion.models import Lote_galleta, Merma_producto
from galletas.models import Galleta
from inventario_insumos.models import Insumo
from .forms import MermaRegistrarForm
from django.contrib.auth.mixins import PermissionRequiredMixin

#Lista de galletas
class ListaGalletasView(PermissionRequiredMixin, TemplateView):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = "lista_galletas_solicitud.html"

    def get_context_data(self, **kwargs):
        # Obtener la fecha actual
        hoy = now().date()

        # Filtrar los lotes caducados y que estan en proceso
        lotes_caducados = Lote_galleta.objects.filter(
            caducidad_lote__lt=hoy,
            estatus='Completado'
        )

        lotes_caducados_detalle = []
        
        # Procesar lotes caducados
        for lote in lotes_caducados:
            # Verificar si ya se ha registrado la merma para este lote de galleta
            if not Merma_producto.objects.filter(id_lote_galleta=lote, motivo='Caducado').exists():
                Merma_producto.objects.create(
                    cantidad=lote.cantidad_galletas,
                    motivo='Caducado',
                    id_lote_galleta=lote
                )
                
                # Actualizar el stock de galletas
                galleta = lote.id_galleta
                galleta.cantidad = max(0, galleta.cantidad - lote.cantidad_galletas)
                galleta.save()
                
            # Actualizar el estatus a cadud¿cado
            if lote.caducidad_lote < hoy and lote.estatus != 'Caducado':
                lote.estatus = 'Caducado'
                lote.save()

            lote.save()

        # Si hay lotes caducados, mostrar mensaje
        if lotes_caducados.exists():
            mensaje = "Los siguientes lotes han caducado:\n" + "\n".join(lotes_caducados_detalle)
            messages.warning(self.request, mensaje)

        lista_galletas = Galleta.objects.all()

        # Verificar que el stock de las galletas no sea menor a 100
        for galleta in lista_galletas:
            if galleta.cantidad < 100:
                messages.warning(self.request, f"Debes preparar más galletas de la {galleta.nombre}")

            # Obtener el último lote de cada galleta
            galleta.ultimo_lote_galleta = (
                Lote_galleta.objects.filter(id_galleta=galleta)
                .order_by('-id_lote_galleta')
                .first()
            )

        # Pasar las galletas y lotes caducados al contexto
        context = super().get_context_data(**kwargs)
        context["lista"] = lista_galletas
        return context


#Lista de produccion
class ListaProduccionView(PermissionRequiredMixin, TemplateView):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = "lista_produccion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = now().date()

        # Aqui se debe de filtrar dos tipos de estatus, completado para que al finalizar produccion no este y de igual forma los caducados
        lotes = Lote_galleta.objects.exclude(estatus__in=["Completado", "Caducado"]).filter(caducidad_lote__gte=hoy)

        #Agregamos mermas de galletas
        for lote in lotes:
            lote.mermas = Merma_producto.objects.filter(id_lote_galleta=lote)

        context["lista"] = lotes
        return context


#Crear un nuevo lote
class CrearLoteView(PermissionRequiredMixin, View):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)

        #Validaciones
        validaciones_creacion_lote = [
            (
                #validar si hay un lote en proceso para que no se creé otro lote de la misma galleta
                Lote_galleta.objects.filter(id_galleta=galleta).exclude(estatus__in=["Completado", "Caducado"]).exists(),
                f"Ya hay un lote en proceso para la galleta {galleta.nombre}, no puedes crear otro hasta que se complete."
            ),
            (
                #validar si hay suficiente stock de galletas, no se podrá crear un nuevo lote
                galleta.cantidad >= 100,
                f"Ya hay suficiente stock ({galleta.cantidad} galletas), no se puede crear otro lote."
            ),
            (
                #validar si la galleta tiene o no insumos
                not galleta.detalle_receta_galleta.exists(),
                "Esta receta no tiene insumos."
            ),
            (
                #Ahora verifica en el inventario de insumos si hay para crear poder crear el lote, si no los hay no se crea el lote
                (insumos_faltantes := [
                    f"{detalle.id_insumo.nombre} (Faltante: {detalle.cantidad - detalle.id_insumo.cantidad})"
                    for detalle in galleta.detalle_receta_galleta.all()
                    if detalle.id_insumo.cantidad < detalle.cantidad
                ]),
                f"Insumos insuficientes: {', '.join(insumos_faltantes)}"
            )
        ]

        # Ejecutamos las validaciones
        for condicion, mensaje in validaciones_creacion_lote:
            if condicion:
                messages.error(request, mensaje)
                return redirect('lista_galletas_solicitud')
        # Crear el lote
        lote = Lote_galleta.objects.create(
            cantidad_galletas=galleta.cantidad_por_lote,
            id_galleta=galleta,
            id_usuario=request.user,
            estatus="Pendiente",
            fecha_preparacion=now()
        )

        # Descontar insumos
        for detalle_receta in galleta.detalle_receta_galleta.all():
            insumo = detalle_receta.id_insumo
            insumo.cantidad -= detalle_receta.cantidad
            insumo.save()

        messages.success(request, f"Lote de {galleta.cantidad_por_lote} galletas creado correctamente.")
        return redirect("lista_produccion")



class ListaLotesCaducadosView(PermissionRequiredMixin, TemplateView):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = "lista_lotes_caducados.html"

    def get_context_data(self, **kwargs):
        hoy = now().date()

        # Filtrar lotes caducados
        lotes_caducados = Lote_galleta.objects.filter(
            caducidad_lote__lt=hoy,
            estatus='Caducado'
        )

        context = super().get_context_data(**kwargs)
        context["lista_caducados"] = lotes_caducados
        return context


# Cambiar estatus de un lote
class CambiarEstatusLote(PermissionRequiredMixin, View):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    def post(self, request, id_lote_galleta):
        lote = get_object_or_404(Lote_galleta, id_lote_galleta=id_lote_galleta)
        nuevo_estatus = request.POST.get('estatus')
        
        if nuevo_estatus == 'Completado':
            # Calcular total de mermas, por ejemplo si en un lote se hacen 50 galletas y se tiraron 10, las que debe de agregar a la cantidad de galleta son 40             
            galletas_disponibles = max(0, lote.cantidad_galletas)
            
            # Actualizar stock de las galletas 
            galleta = lote.id_galleta
            galleta.cantidad += galletas_disponibles
            galleta.save()
            

        lote.estatus = nuevo_estatus
        lote.save()
        return redirect('lista_produccion')


#Agregar Merma
class AgregarMermaView(PermissionRequiredMixin, FormView):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
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
        
        # Descontar la merma de galletas del lote
        lote.cantidad_galletas -= merma.cantidad
        lote.save()

        messages.success(self.request, f"Se registró la merma de {merma.cantidad} galletas del lote {lote.id_lote_galleta}.")
        return super().form_valid(form)