from django.contrib import admin
from django.urls import path
from proovedores.views import CrearProovedorView, ListaProovedorView

urlpatterns = [
    path('crear_proovedor/', CrearProovedorView.as_view(), name='crear_proovedor'),
    path('lista_proovedor/', ListaProovedorView.as_view(), name='lista_proovedor'),
]
