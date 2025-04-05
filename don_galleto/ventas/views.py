from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from ventas.models import Venta, Galleta, Detalle_venta
from ventas.forms import VentaRegistroForms 
from django.db import connection
import datetime
from datetime import timedelta, datetime    
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.db.models import Sum, Count, F
from .models import Venta, Detalle_venta, Galleta

class Lista_Ventas_View(PermissionRequiredMixin, TemplateView):
    permission_required = 'usuarios.empleado'
    def handle_no_permission(self):
        return redirect('home')
    template_name = "lista_ventas.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        ventas = Venta.objects.all()
        detalles_por_venta = {venta.id_venta: [] for venta in ventas}
        totales_por_venta = {venta.id_venta: 0 for venta in ventas}

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM historial_ventas")
            columnas = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                detalle = dict(zip(columnas, row))
                detalles_por_venta[detalle["id_venta"]].append(detalle)
                totales_por_venta[detalle["id_venta"]] += detalle["total"]

        for venta in ventas:
            venta.detalles = detalles_por_venta.get(venta.id_venta, [])
            venta.total = totales_por_venta.get(venta.id_venta, 0)

        context["ventas"] = ventas
        
        pedidos = Venta.objects.filter(tipo__iexact='pedido')
        totales_por_pedido = {pedido.id_venta: 0 for pedido in pedidos}

        with connection.cursor() as cursor:
            cursor.execute("SELECT id_venta, SUM(total) as total FROM ventas_pedido GROUP BY id_venta")
            for row in cursor.fetchall():
                totales_por_pedido[row[0]] = row[1]  

        for pedido in pedidos:
            pedido.total = totales_por_pedido.get(pedido.id_venta, 0)

        context["pedidos"] = pedidos
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ventas_dia")
            columnas = [col[0] for col in cursor.description]
            context["ventas_dia"] = [dict(zip(columnas, row)) for row in cursor.fetchall()]
        
        return context
    
class Generar_Venta_View(PermissionRequiredMixin, FormView):
    permission_required = 'usuarios.empleado'

    def handle_no_permission(self):
        return redirect('home')

    template_name = 'generar_venta.html'
    form_class = VentaRegistroForms
    success_url = reverse_lazy('lista_ventas')

    def form_valid(self, form):
        venta = form.save(commit=False)
        venta.id_usuario = self.request.user

        if venta.tipo == 'fisica':
            venta.estatus = 'confirmado'
        elif venta.tipo == 'pedido':
            venta.estatus = 'pendiente'

        galletas = self.request.POST.getlist('galletas')
        cantidades = self.request.POST.getlist('cantidad')

        for i in range(len(galletas)):
            if galletas[i] and cantidades[i]:
                try:
                    cantidad_vendida = float(cantidades[i])
                    if cantidad_vendida <= 0:
                        form.add_error(None, f"La cantidad de {Galleta.objects.get(id_galleta=galletas[i]).nombre} debe ser mayor a 0.")
                        return self.form_invalid(form)
                except ValueError:
                    form.add_error(None, "Cantidad inválida ingresada.")
                    return self.form_invalid(form)

        for i in range(len(galletas)):
            if galletas[i] and cantidades[i]:
                galleta = Galleta.objects.get(id_galleta=galletas[i])
                cantidad_vendida = float(cantidades[i])

                if cantidad_vendida > galleta.cantidad:
                    form.add_error(None, f"No hay suficiente inventario para {galleta.nombre}. Solo quedan {galleta.cantidad} unidades.")
                    return self.form_invalid(form)

        venta.save()
        for i in range(len(galletas)):
            if galletas[i] and cantidades[i]:
                galleta = Galleta.objects.get(id_galleta=galletas[i])
                cantidad_vendida = float(cantidades[i])

                galleta.cantidad -= cantidad_vendida
                galleta.save()

                Detalle_venta.objects.create(
                    id_venta=venta,
                    id_galleta=galleta,
                    cantidad=cantidad_vendida,
                    precio_galleta=galleta.precio_venta
                )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['galletas'] = Galleta.objects.all()
        return context

def generar_ticket(request, id_venta):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ticket_{id_venta}.pdf"'
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(200, 500))  
    c.setTitle(f"Ticket Don Galleto #{id_venta}")
    c.setFont("Helvetica-Bold", 12)  
    c.drawCentredString(100, 480, "Don Galleto")  
    
    c.setFont("Helvetica", 7) 
    c.drawCentredString(100, 470, "Tienda de Galletas Artesanales")
    c.drawCentredString(100, 460, "Tel: 555-123-4567")
    c.line(50, 450, 150, 450)
    
    c.setFont("Helvetica-Bold", 9) 
    c.drawString(30, 440, f"Ticket #: {id_venta}")
    c.drawString(30, 430, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.line(30, 420, 170, 420)
    
    c.setFont("Helvetica-Bold", 8) 
    c.drawString(30, 410, "CANT")
    c.drawString(60, 410, "DESCRIPCION")  
    c.drawRightString(170, 410, "TOTAL")
    c.line(30, 405, 170, 405)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM ticket WHERE id_venta = %s", [id_venta])
        columnas = [col[0] for col in cursor.description]
        detalles = [dict(zip(columnas, row)) for row in cursor.fetchall()]

    if not detalles:
        return HttpResponse("No hay detalles para esta venta.", status=404)

    y_position = 390 
    c.setFont("Helvetica", 8)  
    for detalle in detalles:
    
        c.drawString(30, y_position, f"{detalle['cantidad']}x")
        
        descripcion = detalle['descripcion'][:20] + "..." if len(detalle['descripcion']) > 20 else detalle['descripcion']
        c.drawString(60, y_position, descripcion)  
        
        c.drawRightString(170, y_position, f"${float(detalle['total']):.2f}")
        
        y_position -= 12  
    
    c.line(30, y_position-5, 170, y_position-5)
    total_venta = sum(d['total'] for d in detalles)
    c.setFont("Helvetica-Bold", 9)  
    c.drawString(100, y_position-15, "TOTAL:")  
    c.drawRightString(170, y_position-15, f"${total_venta:.2f}")
    
    c.line(30, y_position-30, 170, y_position-30)
    c.setFont("Helvetica", 7) 
    c.drawCentredString(100, y_position-40, "¡Gracias por su compra!")
    c.drawCentredString(100, y_position-50, "Vuelva pronto a Don Galleto")
    c.drawCentredString(100, y_position-60, "www.dongalleto.com")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response

def cambiar_estatus(request, venta_id, estatus):
    venta = get_object_or_404(Venta, id_venta=venta_id)
    
    if estatus == 'confirmado':
        venta.estatus = 'confirmado'
    elif estatus == 'cancelado':
        venta.estatus = 'cancelado'
    
    venta.save()
    return redirect('lista_ventas')

def dashboard_ventas(request):
    fecha_limite = datetime.now() - timedelta(days=7)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT SUM(i.precio_unitario * i.cantidad)
            FROM insumo i
            WHERE i.estatus = 'disponible'
        """)
        costo_inventario = cursor.fetchone()[0] or 0

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DATE(v.fecha_venta) as fecha,
                   SUM(dv.cantidad * dv.precio_galleta) as total,
                   COUNT(DISTINCT v.id_venta) as ventas
            FROM venta v
            JOIN detalle_venta dv ON v.id_venta = dv.id_venta_id
            WHERE v.fecha_venta >= %s
            GROUP BY DATE(v.fecha_venta)
            ORDER BY fecha DESC
        """, [fecha_limite])
        ventas_diarias = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.nombre, 
                   SUM(dv.cantidad) as unidades,
                   SUM(dv.cantidad * dv.precio_galleta) as total
            FROM detalle_venta dv
            JOIN galleta g ON dv.id_galleta_id = g.id_galleta
            JOIN venta v ON dv.id_venta_id = v.id_venta
            WHERE v.fecha_venta >= %s
            GROUP BY g.nombre
            ORDER BY total DESC
            LIMIT 5
        """, [fecha_limite])
        productos_vendidos = cursor.fetchall()

    presentaciones_vendidas = Detalle_venta.objects.filter(
        id_venta__fecha_venta__gte=fecha_limite
    ).values(
        'id_galleta__nombre'
    ).annotate(
        cantidad=Sum('cantidad')
    ).order_by('-cantidad')[:5]

    ventas_por_galleta = Detalle_venta.objects.filter(
        id_venta__fecha_venta__gte=fecha_limite
    ).values(
        'id_galleta__nombre'
    ).annotate(
        total_unidades=Sum('cantidad'),
        total_monto=Sum(F('cantidad') * F('precio_galleta'))
    ).order_by('-total_unidades')

    galletas_rentables = Galleta.objects.annotate(
        margen_ganancia=F('precio_venta') - F('costo'),
        rentabilidad=(F('precio_venta') - F('costo')) / F('costo') * 100,
        ganancia_potencial=(F('precio_venta') - F('costo')) * F('cantidad')
    ).order_by('-margen_ganancia')

    ganancia_esperada = sum(g.ganancia_potencial for g in galletas_rentables)

    context = {
        'costo_inventario': costo_inventario,
        'ventas_diarias': ventas_diarias,
        'productos_vendidos': productos_vendidos,
        'presentaciones_vendidas': presentaciones_vendidas,
        'ventas_por_galleta': ventas_por_galleta,
        'ganancia_esperada': ganancia_esperada,
        'galletas_rentables': galletas_rentables,
    }
    
    return render(request, 'dashboards.html', context)