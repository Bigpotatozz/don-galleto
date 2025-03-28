
from django.urls import path
from . import views
from don_galleto.views import IndexView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('listado_galletas/', login_required(views.Lista_galletas_view.as_view()), name='listado_galletas'),
    path('agregar_galleta/', login_required(views.Registrar_galleta_view.as_view()), name = 'registrar_galleta')
]
