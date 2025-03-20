from django.urls import path
from ventas.views import Lista_Ventas_View

urlpatterns = [
    path('lista_ventas/', Lista_Ventas_View.as_view(), name='lista_ventas'),
   
]