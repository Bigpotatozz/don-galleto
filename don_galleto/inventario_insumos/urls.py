
from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('listado_insumos/', login_required(views.Listado_insumos_view.as_view()), name='listado_insumos'),
    path('agregar_insumo/', login_required(views.Registrar_insumo_view.as_view()), name='agregar_insumo'),
    path('registrar_compra_insumo/', login_required(views.Registrar_compra_insumo_view.as_view()), name= 'agregar_compra_insumo'),
    path('registrar_merma_insumo/', login_required(views.Registrar_merma_insumo_view.as_view()), name = "registrar_merma_insumo"),
    path('editar_insumo/<int:id>/', login_required(views.Edicion_insumo_view.as_view()), name = 'editar_insumo')
]
