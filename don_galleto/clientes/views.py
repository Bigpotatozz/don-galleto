from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, DetailView, ListView
from django.contrib.auth import logout
from django.views import View
from galletas.models import Galleta
from ventas.models import Venta, Detalle_venta
from django.contrib import messages
from usuarios.utils import asignar_permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
import json
import logging


class Lista_galletas_view(TemplateView):
    template_name = 'lista_galletas.html'
    
    def get_context_data(self):
        galletas = Galleta.objects.all()
        return {
            "galletas": galletas
        }
    
class AgregarAlCarrito(TemplateView):
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        carrito = request.session.get('carrito', {})

        data = json.loads(request.body.decode('utf-8'))
        presentacion = data.get('presentacion', 'Individual')  # Corregido para obtener la presentación desde JSON

        logging.debug(f"Presentación seleccionada: {presentacion}")

        multiplicador = 1
        if presentacion == 'Caja':
            multiplicador = 50
        elif presentacion == 'Bolsa':
            multiplicador = 15

        if str(id_galleta) in carrito:
            carrito[str(id_galleta)]['cantidad'] += multiplicador
        else:
            carrito[str(id_galleta)] = {
                'nombre': galleta.nombre,
                'precio_venta': galleta.precio_venta,
                'cantidad': multiplicador,
                'presentacion': presentacion,
            }

        request.session['carrito'] = carrito

        carrito_lista = list(carrito.values())
        carrito_total = sum(item['precio_venta'] * item['cantidad'] for item in carrito_lista)
        
        historial_compras = request.session.get('historial_compras', [])
        compra = {
            'productos': carrito_lista,
            'total': carrito_total
        }

        historial_compras.append(compra)
        request.session['historial_compras'] = historial_compras

        return JsonResponse({'galleta': list(carrito.values()), 'carrito_total': carrito_total})

class GuardarCarritoView(LoginRequiredMixin, TemplateView):
    template_name = 'guardar_carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        carrito = self.request.session.get('carrito', {})
        carrito_lista = list(carrito.values())
        carrito_total = sum(item['precio_venta'] * item['cantidad'] for item in carrito_lista)

        context.update({
            'carrito': carrito_lista,
            'total': carrito_total,
        })

        return context

    def post(self, request, *args, **kwargs):
        galletas_ids = request.POST.getlist('id_galleta')
        cantidades = request.POST.getlist('cantidad')
        presentaciones = request.POST.getlist('presentacion')

        carrito = request.session.get('carrito', {})

        for galleta_id, cantidad, presentacion in zip(galletas_ids, cantidades, presentaciones):
            if galleta_id in carrito:
                carrito[galleta_id]['cantidad'] += int(cantidad)
            else:
                carrito[galleta_id] = {
                    'nombre': f'Galleta {galleta_id}',  
                    'cantidad': int(cantidad),
                    'presentacion': presentacion,
                }

        request.session['carrito'] = carrito
        messages.success(request, 'Carrito actualizado correctamente.')

        return redirect('detalle_compra')  

class EliminarDelCarritoView(LoginRequiredMixin, View):
    def post(self, request, id_galleta):
        carrito = request.session.get('carrito', {})
        if str(id_galleta) in carrito:
            del carrito[str(id_galleta)]
            request.session['carrito'] = carrito
            messages.success(request, 'Galleta eliminada del carrito.')
        else:
            messages.error(request, 'Galleta no encontrada en el carrito.')

        return redirect('detalle_compra')

class DetalleCompraView(LoginRequiredMixin, TemplateView):
    template_name = 'detalle_compra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        carrito = self.request.session.get('carrito', {})
        carrito_lista = list(carrito.values())
        carrito_total = sum(item['precio_venta'] * item['cantidad'] for item in carrito_lista)

        context.update({
            'carrito': carrito_lista,
            'total': carrito_total,
        })

        return context

class FinalizarCompraView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carrito = request.session.get('carrito', {})
        if not carrito:
            messages.error(request, 'El carrito está vacío.')
            return redirect('lista_galletas')
        
        total = sum(item['precio_venta'] * item['cantidad'] for item in carrito.values())

        venta = Venta.objects.create(
            id_usuario=request.user,
            fecha_venta=now(),
            estatus='En proceso',
            tipo='pedido',
            total=total,
        )

        for galleta_id, item in carrito.items():
            Detalle_venta.objects.create(
                id_venta=venta,
                id_galleta_id=galleta_id,
                cantidad=item['cantidad'],
                precio_galleta=item['precio_venta'],
                tipo_unidad=item['presentacion'],
            )

        galleta = Galleta.objects.get(id_galleta= galleta_id)
        if galleta.cantidad >= item['cantidad']:
            galleta.cantidad -= item['cantidad']
            galleta.save()
        else:
            messages.error(request, f'No hay suficiente stock para completar la compra.')
            return redirect('detalle_compra')

        request.session['carrito'] = {}

        messages.success(request, 'Compra finalizada con éxito.')
        return redirect('listado_galletas')  

class HistorialComprasView(LoginRequiredMixin, TemplateView):
    template_name = 'historial_compras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = Venta.objects.filter(id_usuario=self.request.user, estatus='Completada').order_by('-fecha_venta')

        ventas_con_totales = []
        for venta in venta:
            total = sum(detalle.precio_galleta * detalle.cantidad for detalle in venta.detalle_venta_venta.all())
            ventas_con_totales.append({
                'venta': venta,
                'total': total,
            })
        context['ventas_con_totales'] = ventas_con_totales
        return context