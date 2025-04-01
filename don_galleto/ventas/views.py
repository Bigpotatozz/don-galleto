from django.shortcuts import render
from django.db import connection
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .models import Venta, Detalle_venta, Galleta

def dashboard_ventas(request):
    fecha_limite = datetime.now() - timedelta(days=7)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DATE(fecha_venta) as fecha, 
                   SUM(total) as total_ventas, 
                   COUNT(*) as cantidad_ventas
            FROM venta
            WHERE fecha_venta >= %s
            GROUP BY DATE(fecha_venta)
            ORDER BY fecha DESC
        """, [fecha_limite])
        ventas_diarias = cursor.fetchall()
    
    productos_vendidos = Detalle_venta.objects.filter(
        id_venta__fecha_venta__gte=fecha_limite  
    ).values(
        'id_galleta__nombre'  
    ).annotate(
        total_vendido=Sum('cantidad'),
        total_ventas=Sum('precio_galleta')  
    ).order_by('-total_vendido')[:5]
    
    presentaciones_vendidas = Detalle_venta.objects.filter(
        id_venta__fecha_venta__gte=fecha_limite
    ).values(
        'id_galleta__peso_unidad'  
    ).annotate(
        cantidad_vendida=Sum('cantidad')
    ).order_by('-cantidad_vendida')[:5]
    
    context = {
        'ventas_diarias': ventas_diarias,
        'productos_vendidos': productos_vendidos,
        'presentaciones_vendidas': presentaciones_vendidas,
    }
    
    return render(request, 'dashboard_ventas.html', context)

