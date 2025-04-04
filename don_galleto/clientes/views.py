from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
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
from django.utils.decorators import method_decorator


class Lista_galletas_catalogo_view(TemplateView):
    template_name = 'catalogo_galletas.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        galletas = Galleta.objects.all()

        carrito = self.request.session.get('carrito', {})
        carrito_lista = list(carrito.values())

        for item in carrito_lista:
            item['subtotal'] = item['precio_venta'] * item['cantidad']

        carrito_total = sum(item['precio_venta'] * item['cantidad'] for item in carrito_lista)

        context.update ({
            "galletas": galletas,
            "carrito": carrito,
            "total_carrito": carrito_total,
        })
        return context
    
@method_decorator(login_required, name='dispatch')
class AgregarAlCarrito(TemplateView):
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        carrito = request.session.get('carrito', {})

        data = json.loads(request.body.decode('utf-8'))
        presentacion = data.get('presentacion', 'Individual') 
        cantidad = data.get('cantidad', 1)

        if cantidad < 1:
            return JsonResponse({'error': 'La cantidad debe ser al menos 1.'}, status=400)

        logging.debug(f"Presentación seleccionada: {presentacion}")
        logging.debug(f"Cantidad seleccionada: {cantidad}")

        multiplicador = 1
        if presentacion == 'Caja':
            multiplicador = 50
        elif presentacion == 'Bolsa':
            multiplicador = 15

        cantidad_total = cantidad * multiplicador

        if galleta.cantidad < cantidad_total:
            return JsonResponse({'error': 'No hay suficiente stock para completar la compra.'}, status=400)

        # Si el producto ya está en el carrito, actualizamos la cantidad
        if str(id_galleta) in carrito:
            carrito[str(id_galleta)]['cantidad'] += cantidad_total
        else:
            carrito[str(id_galleta)] = {
                'id_galleta': galleta.id_galleta,
                'nombre': galleta.nombre,
                'precio_venta': galleta.precio_venta,
                'cantidad': cantidad_total,
                'presentacion': presentacion,
            }

        # 🔥 **Siempre recalculamos los subtotales para todos los productos** 🔥
        for item in carrito.values():
            item['subtotal'] = item['precio_venta'] * item['cantidad']

        request.session['carrito'] = carrito

        carrito_lista = list(carrito.values())
        carrito_total = sum(item['subtotal'] for item in carrito.values())

        historial_compras = request.session.get('historial_compras', [])
        compra = {
            'productos': carrito_lista,
            'total': carrito_total
        }

        historial_compras.append(compra)
        request.session['historial_compras'] = historial_compras

        return JsonResponse({'galleta': carrito_lista, 'carrito_total': carrito_total})


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
            messages.error(request, 'No puedes realizar una compra sin seleccionar un producto.')
            return redirect('detalle_compra')
        
        total = sum(item['precio_venta'] * item['cantidad'] for item in carrito.values())

        venta = Venta.objects.create(
            fecha_venta=now(),
            estatus='Pendiente',
            tipo='pedido',
            id_usuario_id = request.user.id_usuario
        )

        for galleta_id, item in carrito.items():
            Detalle_venta.objects.create(
                id_venta_id = venta.id_venta,
                id_galleta_id = galleta_id,
                cantidad=item['cantidad'],
                precio_galleta=item['precio_venta'],
                presentacion = item['presentacion'],
            )

        galleta = Galleta.objects.get(id_galleta= galleta_id)
        if galleta.cantidad >= item['cantidad']:
            galleta.cantidad -= item['cantidad']
            galleta.save()
        else:
            messages.error(request, f'No hay suficiente stock para completar la compra.')
            return redirect('detalle_compra')

        request.session['carrito'] = {}
        return redirect('gracias')  

class HistorialComprasView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    permission_required = "usuarios.cliente"
    template_name = 'historial_compras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas = Venta.objects.filter(id_usuario=self.request.user).order_by('-fecha_venta')

        ventas_con_detalles = []
        for venta in ventas:
            detalles = []
            for detalle in venta.detalle_venta_venta.all():
                detalles.append({
                    'id_galleta': detalle.id_galleta,
                    'cantidad': detalle.cantidad,
                    'precio_galleta': detalle.precio_galleta,
                    'total': detalle.cantidad * detalle.precio_galleta,  
                })
            total_venta = sum(detalle['total'] for detalle in detalles)
            ventas_con_detalles.append({
                'venta': venta,
                'detalles': detalles,
                'total': total_venta,
            })

        context['ventas_con_detalles'] = ventas_con_detalles
        return context
    
class ActualizarCarritoView(LoginRequiredMixin, View):
    def post(self, request, id_galleta):
        carrito = request.session.get('carrito', {})
        data = json.loads(request.body.decode('utf-8'))
        accion = data.get('accion')

        if str(id_galleta) in carrito:
            if accion == 'aumentar':
                carrito[str(id_galleta)]['cantidad'] += 1
            elif accion == 'disminuir' and carrito[str(id_galleta)]['cantidad'] > 1:
                carrito[str(id_galleta)]['cantidad'] -= 1
            else:
                return JsonResponse({'success': False, 'message': 'Acción no válida.'}, status=400)

            request.session['carrito'] = carrito
            return JsonResponse({'success': True, 'carrito': carrito})
        else:
            return JsonResponse({'success': False, 'message': 'Producto no encontrado en el carrito.'}, status=404)
        

class ObtenerCarritoView(View):
    def get(self, request):
        carrito = request.session.get('carrito', {})
        for item in carrito.values():
            item['subtotal'] = item['precio_venta'] * item['cantidad']
        return JsonResponse({"carrito": carrito})
    
class EliminarDelCarritoView(View):
    def post(self, request, id_galleta):
        carrito = request.session.get('carrito', {})
        print(f"Carrito antes de eliminar: {carrito}")  

        if str(id_galleta) in carrito:
            del carrito[str(id_galleta)]
            request.session['carrito'] = carrito
            total = sum(item['precio_venta'] * item['cantidad'] for item in carrito.values())
            print(f"Carrito después de eliminar: {carrito}")  
            return JsonResponse({'success': True, 'total': total, 'carrito': carrito})

        return JsonResponse({'success': False, 'message': 'Producto no encontrado en el carrito.'}, status=404)
    
class GraciasView(TemplateView):
    template_name = 'gracias.html'

    def get(self, request, *args, **kwargs):
        request.session['carrito'] = {}
        return super().get(request, *args, **kwargs)


    