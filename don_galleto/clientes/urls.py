from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
from .views import  Lista_galletas_view, DetalleCompraView, AgregarAlCarrito, HistorialComprasView


urlpatterns = [
    path('listado_galletas/', login_required(Lista_galletas_view.as_view()), name='listado_galletas'),
    path('detalle_galletas/<int:pk>/', login_required(DetalleCompraView.as_view()), name='detalle_galletas'),
    path('agregar/<int:id_galleta>/', AgregarAlCarrito.as_view(), name='agregar_al_carrito'),
    path('historial_compras/', HistorialComprasView.as_view(), name='historial_compras'),
    path('detalle_compra/', DetalleCompraView.as_view(), name='detalle_compra'),
    path('finalizar_compra/', views.FinalizarCompraView.as_view(), name='finalizar_compra'),
]