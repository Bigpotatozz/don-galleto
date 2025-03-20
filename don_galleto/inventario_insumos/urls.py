
from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('listado_insumos/', login_required(views.Listado_insumos_view.as_view()), name='listado_insumos'),
    path('agregar_insumo/', login_required(views.Registrar_insumo_view.as_view()), name='agregar_insumo'),
]
