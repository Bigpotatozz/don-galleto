from django.urls import path
from .views import ListaGalletasRecetaView

urlpatterns = [
    path('listado_galletas_receta/', ListaGalletasRecetaView.as_view(), name="listado_galletas_solicitud")
]


