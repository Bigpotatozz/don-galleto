from django.urls import path
from .views import ListaGalletasView, CrearLoteView,ListaProduccionView, CambiarEstatusLote, AgregarMermaView, ListaLotesCaducadosView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('lista_galletas_solicitud/', login_required(ListaGalletasView.as_view()), name='lista_galletas_solicitud'),
    path('crear_lote/<int:id_galleta>/', login_required(CrearLoteView.as_view()), name='crear_lote_galleta'),
    path('lista_produccion/', login_required(ListaProduccionView.as_view()), name='lista_produccion'),
    path('produccion/cambiar_estatus/<int:id_lote_galleta>/', login_required(CambiarEstatusLote.as_view()), name='actualizar_estatus_lote'),
    path('agregar_merma/<int:id_lote_galleta>/', login_required(AgregarMermaView.as_view()), name='agregar_merma'),
    path('lotes_caducados/', login_required(ListaLotesCaducadosView.as_view()), name='lista_lotes_caducados'),
]

