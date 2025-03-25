from django.urls import path
from .views import ListaGalletasView, CrearLoteView,ListaProduccionView, CambiarEstatusLote, AgregarMermaView

urlpatterns = [
    path('lista_galletas/', ListaGalletasView.as_view(), name='lista_galletas'),
    path('crear_lote/<int:id_galleta>/', CrearLoteView.as_view(), name='crear_lote_galleta'),
    path('lista_produccion/', ListaProduccionView.as_view(), name='lista_produccion'),
    path('produccion/cambiar_estatus/<int:id_lote_galleta>/', CambiarEstatusLote.as_view(), name='actualizar_estatus_lote'),
    path('agregar_merma/<int:id_lote_galleta>/', AgregarMermaView.as_view(), name='agregar_merma'),
]

