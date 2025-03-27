from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView, DetailView, ListView
from django.contrib.auth import logout
from django.views import View
from galletas.models import Galleta
from usuarios.utils import asignar_permisos

class Lista_galletas_view(TemplateView):
    template_name = 'lista_galletas.html'
    
    def get_context_data(self):
        galletas = Galleta.objects.all()
        return {
            "galletas": galletas
        }

class DetalleGalletaView(DetailView):
    model = Galleta
    template_name = 'detalle_galleta.html'
    context_object_name = 'galleta'

    def post(self, request, *args, **kwargs):
        galleta = self.get_object()
        cantidad = int(request.POST.get('cantidad', 1))

        Compra.objects.create(user=request.user, galleta=galleta, cantidad=cantidad)
        
        print(f"Compra realizada: {galleta.nombre} - Cantidad: {cantidad}")

        return HttpResponseRedirect(reverse('detalle_galleta', args=[galleta.id]))

class AgregarAlCarrito(TemplateView):
    def post(self, request, id_galleta):
        galleta = get_object_or_404(Galleta, id_galleta=id_galleta)
        carrito = request.session.get('carrito', {})

        if str(id_galleta) in carrito:
            carrito[str(id_galleta)]['cantidad'] += 1
        else:
            carrito[str(id_galleta)] = {
                'nombre': galleta.nombre,
                'precio_venta': galleta.precio_venta,
                'cantidad': 1
            }

            

        request.session['carrito'] = carrito

        carrito_lista = list (carrito.values())

        carrito_total = sum(item['precio_venta'] * item['cantidad'] for item in carrito_lista)
        
        historial_compras = request.session.get('historial_compras', [])
        compra = {
            'productos': carrito_lista,  
            'total': carrito_total        
        }

        historial_compras.append(compra)
        request.session['historial_compras'] = historial_compras

        return JsonResponse({'galleta': list(carrito.values()), 'carrito_total': carrito_total})
    
class carrito_view(TemplateView):
    template_name = 'ver_carrito.html'
    
    def get_context_data(self):
        galletas = Galleta.objects.all()
        return {
            "galletas": galletas
        }

class historial_compras(TemplateView):
    template_name = 'historial_compras.html'

    def get_context_data(self):
        historial = self.request.session.get('historial_compras', [])
        return {
            "compras": historial
        }