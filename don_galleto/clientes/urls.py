from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
from .views import  Lista_galletas_catalogo_view, DetalleCompraView, AgregarAlCarrito, HistorialComprasView, EliminarDelCarritoView, ActualizarCarritoView, EliminarDelCarritoView, ObtenerCarritoView


urlpatterns = [
    path('catalogo_galletas/', login_required(Lista_galletas_catalogo_view.as_view()), name='catalogo_galletas'),
    path('agregar/<int:id_galleta>/', login_required(AgregarAlCarrito.as_view()), name='agregar_al_carrito'),
    path('detalle_compra/', login_required(DetalleCompraView.as_view()), name='detalle_compra'),
    path('finalizar_compra/', views.FinalizarCompraView.as_view(), name='finalizar_compra'),
    path('historial_compras/', login_required(HistorialComprasView.as_view()), name='historial_compras'),
    path('actualizar/<int:id_galleta>/', login_required(ActualizarCarritoView.as_view()), name='actualizar_carrito'),
    path('eliminar/<int:id_galleta>/', EliminarDelCarritoView.as_view(), name='eliminar_carrito'),
    path('obtener_carrito/', ObtenerCarritoView.as_view(), name='obtener_carrito'),
]