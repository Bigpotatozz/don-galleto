from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=15, choices=[
        ('activo', 'Activo'),
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ])

    class Meta:
        db_table = 'carrito'

class ItemCarrito(models.Model):
    PRESENTACIONES = [
        ('unidad', 'Por unidad'),
        ('gramos', 'Por gramos'),
        ('700g', 'Paquete 700g'),
        ('1kg', 'Paquete 1kg')
    ]
    
    id_item = models.AutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    galleta = models.ForeignKey('galletas.Galleta', on_delete=models.CASCADE)
    cantidad = models.FloatField(validators=[MinValueValidator(0.1)])
    presentacion = models.CharField(max_length=10, choices=PRESENTACIONES)
    fecha_recoger = models.DateField()

    class Meta:
        db_table = 'item_carrito'