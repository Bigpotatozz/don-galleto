
from django.contrib import admin
from django.urls import path

from . import views
from don_galleto.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    #path('inventario_galletas/'),
    #path('inventario_insumos/'),
    #path('overview/'),
    #path('produccion/'),
    #path('proovedores/'),
    #path('recetas/'),
    #path('tienda/'),
    #path('usuarios/'),
    #path('ventas/'),
    #path('clientes/'),
]
