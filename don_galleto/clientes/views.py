from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from .models import Carrito, ItemCarrito
from .forms import AgregarAlCarritoForm, ConfirmarPedidoForm
from galletas.models import Galleta
from ventas.models import Venta, Detalle_venta
from datetime import date

class GalletasDisponiblesView(LoginRequiredMixin, ListView):
    model = Galleta
    template_name = 'lista_galletas.html'
    context_object_name = 'galletas'
    
    def get_queryset(self):
        return Galleta.objects.filter(cantidad__gt=0)

class CarritoView(LoginRequiredMixin, DetailView):
    model = Carrito
    template_name = 'carrito.html'
    
    def get_object(self):
        carrito, created = Carrito.objects.get_or_create(
            usuario=self.request.user,
            estatus='activo'
        )
        return carrito
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito = self.get_object()
        context['total'] = sum(
            item.galleta.precio_venta * item.cantidad 
            for item in carrito.items.all()
        )
        context['confirmar_form'] = ConfirmarPedidoForm()
        return context

class AgregarAlCarritoView(LoginRequiredMixin, CreateView):
    model = ItemCarrito
    form_class = AgregarAlCarritoForm
    template_name = 'agregar_al_carrito.html'
    
    def get_success_url(self):
        return reverse_lazy('ver_carrito')
    
    def get_initial(self):
        initial = super().get_initial()
        galleta_id = self.kwargs.get('galleta_id')
        if galleta_id:
            initial['galleta'] = get_object_or_404(Galleta, id=galleta_id)
        return initial
    
    def form_valid(self, form):
        carrito, created = Carrito.objects.get_or_create(
            usuario=self.request.user,
            estatus='activo'
        )
        
        galleta = form.cleaned_data['galleta']
        presentacion = form.cleaned_data['presentacion']
        cantidad = form.cleaned_data['cantidad']
        
        item_existente = ItemCarrito.objects.filter(
            carrito=carrito,
            galleta=galleta,
            presentacion=presentacion,
            fecha_recoger=form.cleaned_data['fecha_recoger']
        ).first()
        
        if item_existente:
            item_existente.cantidad += cantidad
            item_existente.save()
        else:
            form.instance.carrito = carrito
            form.save()
        
        messages.success(self.request, f"{galleta.nombre} agregado al carrito")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al agregar el producto al carrito")
        return super().form_invalid(form)

class EliminarDelCarritoView(LoginRequiredMixin, DeleteView):
    model = ItemCarrito
    success_url = reverse_lazy('ver_carrito')
    
    def get_queryset(self):
        return ItemCarrito.objects.filter(carrito__usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Producto eliminado del carrito")
        return super().delete(request, *args, **kwargs)

class ConfirmarPedidoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ConfirmarPedidoForm(request.POST)
        carrito = get_object_or_404(
            Carrito,
            usuario=request.user,
            estatus='activo'
        )
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    venta = Venta.objects.create(
                        fecha_venta=date.today(),
                        tipo='pedido',
                        estatus='pendiente',
                        id_usuario=request.user,
                        total=sum(item.galleta.precio_venta * item.cantidad for item in carrito.items.all())
                    )

                    for item in carrito.items.all():
                        Detalle_venta.objects.create(
                            cantidad=item.cantidad,
                            id_venta=venta,
                            id_galleta=item.galleta,
                            presentacion=item.presentacion,
                            precio_galleta=item.galleta.precio_venta
                        )

                    carrito.estatus = 'completado'
                    carrito.save()
                    
                    messages.success(request, "Pedido confirmado correctamente")
                    return redirect('historial_pedidos')
            
            except Exception as e:
                messages.error(request, f"Error al confirmar pedido: {str(e)}")
                return redirect('ver_carrito')
        
        messages.error(request, "Formulario inválido")
        return redirect('ver_carrito')

class HistorialPedidosView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'historial_pedidos.html'
    context_object_name = 'ventas'
    
    def get_queryset(self):
        return Venta.objects.filter(
            id_usuario=self.request.user,
            tipo='pedido'
        ).order_by('-fecha_venta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for venta in context['ventas']:
            venta.detalles = Detalle_venta.objects.filter(id_venta=venta)
        return context
    
class GalletasPublicasView(ListView):
    """Vista pública para listar galletas disponibles"""
    model = Galleta
    template_name = 'lista_galletas_publica.html'
    context_object_name = 'galletas'
    
    def get_queryset(self):
        return Galleta.objects.filter(cantidad__gt=0).order_by('nombre')