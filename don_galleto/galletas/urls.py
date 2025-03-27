from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
from galletas.views import  Lista_galletas_view, DetalleGalletaView, AgregarAlCarrito, carrito_view

urlpatterns = [
    path('listado_galletas/', login_required(views.Lista_galletas_view.as_view()), name='listado_galletas'),
    path('detalle_galletas/<int:pk>/', login_required(DetalleGalletaView.as_view()), name='detalle_galletas'),
    path('agregar/<int:id_galleta>/', AgregarAlCarrito.as_view(), name='agregar_al_carrito'),
]