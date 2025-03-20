
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import os
from . import views
from don_galleto.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('users/registro/', views.registro, name='registro'),
    path('users/', include("django.contrib.auth.urls")),
    path('usuarios/', include('usuarios.urls')),
    path('clientes/', include('clientes.urls')),
    
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
