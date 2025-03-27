from django.urls import path
from .views import AgregarGalletaRecetaView, ListaGalletasRecetaView, SeleccionarInsumosView, DetallesGalletaView, EditarGalletaRecetaView, EditarInsumosRecetaView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('agregar_galleta_receta/', login_required(AgregarGalletaRecetaView.as_view()), name='agregar_galleta_receta'),
    path('lista_galletas_receta/', login_required(ListaGalletasRecetaView.as_view()), name='lista_galletas_receta'),
    path('seleccionar_insumos_receta/<int:id_galleta>/', login_required(SeleccionarInsumosView.as_view()), name='seleccionar_insumos_receta'),
    path('detalles_galleta_receta/<int:id_galleta>/', login_required(DetallesGalletaView.as_view()), name='detalles_galleta_receta'),
    path('editar_galleta_receta/<int:id_galleta>/', login_required(EditarGalletaRecetaView.as_view()), name='editar_galleta_receta'),
    path('editar_insumos_receta/<int:id_galleta>/', login_required(EditarInsumosRecetaView.as_view()), name='editar_insumos_receta'),

]
