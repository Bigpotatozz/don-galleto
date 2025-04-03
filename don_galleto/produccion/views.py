from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView, View
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib import messages
from produccion.models import Lote_galleta, Merma_producto
from galletas.models import Galleta
from inventario_insumos.models import Insumo
from .forms import MermaRegistrarForm, LoteGalletaForm
from django.contrib.auth.mixins import PermissionRequiredMixin

#Lista de galletas
class ListaGalletasView(PermissionRequiredMixin, TemplateView):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = "lista_galletas_solicitud.html"

    def get_context_data(self):
        lista = Galleta.objects.all()
        for galleta in lista:
            if galleta.cantidad < 100:
                messages.warning(self.request, f"Debes preparar más galletas de la {galleta.nombre}")
        
        for galleta in lista:
            ultimo_lote = Lote_galleta.objects.filter(id_galleta=galleta).order_by('-fecha_preparacion').first()
            galleta.ultimo_lote = ultimo_lote
        return {
            "lista": lista
        }



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
class CrearLoteView(View):
    def get(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        form = LoteGalletaForm(galleta=galleta)  # Pasamos solo la galleta
        return render(request, 'lista_produccion.html', {'form': form, 'galleta': galleta})

    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        form = LoteGalletaForm(request.POST, galleta=galleta) 

        if form.is_valid():
            # Guardar el lote si el formulario es válido
            form.guardar_lote_galleta(request.user)
            messages.success(request, f"Lote de {galleta.cantidad_receta} galletas creado correctamente.")
            return redirect('lista_produccion')
        else:
            # Mostrar los errores de validación
            for error in form.errors.values():
                messages.error(request, error)

            return redirect('lista_galletas_solicitud')


    
class ListaLotesView(TemplateView):
    permission_required = 'usuarios.empleado'
        
    def handle_no_permission(self):
        return redirect('home')
    
    template_name = "lista_lotes.html"
    
    def get_context_data(self, **kwargs):
        # Obtener la fecha actual
        hoy = now().date()

        # Filtrar los lotes caducados que han sido completados
        lotes_caducados = Lote_galleta.objects.filter(
            caducidad_lote__lt=hoy,
            estatus='Completado'
        )

        lotes_caducados_detalle = []

        # Procesar los lotes caducados
        for lote in lotes_caducados:
            # Verificar si ya se ha registrado la merma para este lote de galleta
            if not Merma_producto.objects.filter(id_lote_galleta=lote, motivo='Caducado').exists():
                # Registrar la merma por caducidad
                Merma_producto.objects.create(
                    cantidad=lote.cantidad_galletas,
                    motivo='Caducado',
                    id_lote_galleta=lote
                )
                
                # Actualizar el stock de galletas (restar la cantidad del lote caducado)
                galleta = lote.id_galleta
                galleta.cantidad = max(0, galleta.cantidad - lote.cantidad_galletas)
                galleta.save()
                
            # Cambiar el estatus del lote a 'Caducado'
            if lote.caducidad_lote < hoy and lote.estatus != 'Caducado':
                lote.estatus = 'Caducado'
                lote.save()

            # Agregar detalle del lote caducado a la lista
            lotes_caducados_detalle.append(f"Lote {lote.id_lote_galleta} de la galleta {lote.id_galleta.nombre}")

        # Si hay lotes caducados, enviar una alerta con los detalles
        if lotes_caducados.exists():
            mensaje = "Los siguientes lotes han caducado:\n" + "\n".join(lotes_caducados_detalle)
            messages.warning(self.request, mensaje)

        # Obtener todos los lotes, incluyendo su estatus
        lotes = Lote_galleta.objects.all()

        # Pasar los lotes caducados y no caducados al contexto
        context = super().get_context_data(**kwargs)
        context["lotes"] = lotes  # Esto lo pasamos como 'lotes' al template
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
        messages.success(request, f"El estatus del lote ha sido cambiado a {nuevo_estatus}.")
        
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