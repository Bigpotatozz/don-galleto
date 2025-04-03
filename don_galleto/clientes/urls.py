from django.urls import path
from .views import (GalletasPublicasView,CarritoView,AgregarAlCarritoView,EliminarDelCarritoView,ConfirmarPedidoView,HistorialPedidosView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
        path('galletas/', GalletasPublicasView.as_view(), name='galletas_disponibles'),
    path('carrito/', login_required(CarritoView.as_view()), name='ver_carrito'),
    path('agregar/<int:galleta_id>/', login_required(AgregarAlCarritoView.as_view()), name='agregar_al_carrito'),
    path('eliminar/<int:pk>/', login_required(EliminarDelCarritoView.as_view()), name='eliminar_del_carrito'),
    path('confirmar-pedido/', login_required(ConfirmarPedidoView.as_view()), name='confirmar_pedido'),
    path('historial/', login_required(HistorialPedidosView.as_view()), name='historial_pedidos'),
]