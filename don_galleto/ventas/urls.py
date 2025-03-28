from django.urls import path
from ventas.views import Lista_Ventas_View, Generar_Venta_View, generar_ticket

urlpatterns = [
    path('lista_ventas/', Lista_Ventas_View.as_view(), name='lista_ventas'),
    path('generar_venta/', Generar_Venta_View.as_view(), name='generar_venta'),
    path('generar_ticket/<int:id_venta>/', generar_ticket, name='generar_ticket'),
   
] 


