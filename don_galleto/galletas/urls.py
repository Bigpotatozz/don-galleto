<<<<<<< HEAD
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

=======

from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('listado_galletas/', login_required(views.Lista_galletas_view.as_view()), name='listado_galletas'),
    path('agregar_galleta/', login_required(views.Registrar_galleta_view.as_view()), name = 'registrar_galleta')
>>>>>>> 41544858cbbcb5a5c4e98f3b02f1186925d54593
]
