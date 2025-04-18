from django.db import models
from usuarios.models import Usuario
from galletas.models import Galleta
# Create your models here.
class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateField()
    tipo = models.CharField(max_length=30)
    estatus = models.CharField(max_length=30)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, related_name='venta_cliente')
    
    class Meta:
        db_table = 'venta'
    def __str__(self):
        return f" {self.fecha_venta} - {self.total} - {self.tipo} - {self.estatus} - {self.id_usuario}"
    
    
class Detalle_venta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    cantidad = models.FloatField()
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=False, related_name='detalle_venta_venta')
    id_galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=False, related_name='detalle_venta_galleta')
    precio_galleta = models.FloatField(null=False)
    presentacion = models.CharField(max_length=15, default='unidad', null=False)

    class Meta:
        db_table = 'detalle_venta'
    
    def save(self, *args, **kwargs):
        self.precio_galleta = self.id_galleta.precio_venta
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f" {self.cantidad} - {self.id_venta} - {self.id_galleta}"