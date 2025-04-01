from django.urls import path
from ventas.views import Lista_Ventas_View, Generar_Venta_View, generar_ticket, cambiar_estatus

urlpatterns = [
    path('lista_ventas/', Lista_Ventas_View.as_view(), name='lista_ventas'),
    path('generar_venta/', Generar_Venta_View.as_view(), name='generar_venta'),
    path('generar_ticket/<int:id_venta>/', generar_ticket, name='generar_ticket'),
    path('venta/<int:venta_id>/<str:estatus>/cambiar_estatus/', cambiar_estatus, name='cambiar_estatus'),
] 

