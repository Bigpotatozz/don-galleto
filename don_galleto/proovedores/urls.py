from django.contrib import admin
from django.urls import path
from proovedores.views import CrearProovedorView, ListaProovedorView, EditarProovedorView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('crear_proovedor/', login_required(CrearProovedorView.as_view()), name='crear_proovedor'),
    path('lista_proovedor/', login_required(ListaProovedorView.as_view()), name='lista_proovedor'),
    path('editar_proovedor/<int:id>/', login_required(EditarProovedorView.as_view()), name='editar_proovedor'),
]
