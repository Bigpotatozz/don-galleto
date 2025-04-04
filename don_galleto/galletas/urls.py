from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
from galletas.views import  Lista_galletas_view, Registrar_galleta_view, Editar_galleta_view
urlpatterns = [
    path('listado_galletas/', login_required(views.Lista_galletas_view.as_view()), name='listado_galletas'),
    path('agregar_galleta/', login_required(views.Registrar_galleta_view.as_view()), name = 'registrar_galleta'),
    path('editar_galleta/<int:id>/', login_required(views.Editar_galleta_view.as_view()), name = 'editar_galleta')
]
