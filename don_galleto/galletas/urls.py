from django.urls import path
from .views import AgregarGalletaRecetaView, ListaGalletasRecetaView, SeleccionarInsumosView, DetallesGalletaView, EditarGalletaRecetaView, EditarInsumosRecetaView

urlpatterns = [
    path('agregar_galleta_receta/', AgregarGalletaRecetaView.as_view(), name='agregar_galleta_receta'),
    path('lista_galletas_receta/', ListaGalletasRecetaView.as_view(), name='lista_galletas_receta'),
    path('seleccionar_insumos_receta/<int:id_galleta>/', SeleccionarInsumosView.as_view(), name='seleccionar_insumos_receta'),
    path('detalles_galleta_receta/<int:id_galleta>/', DetallesGalletaView.as_view(), name='detalles_galleta_receta'),
    path('editar_galleta_receta/<int:id_galleta>/', EditarGalletaRecetaView.as_view(), name='editar_galleta_receta'),
    path('editar_insumos_receta/<int:id_galleta>/', EditarInsumosRecetaView.as_view(), name='editar_insumos_receta'),

]
