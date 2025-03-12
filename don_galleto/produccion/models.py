from django.db import models
from galletas.models import Galleta
from usuarios.models import Usuario

# Create your models here.
class Lote_galleta(models.Model):
    id_lote_galleta = models.AutoField(primary_key=True)
    fecha_preparacion = models.DateField()
    estatus = models.CharField(max_length=10)
    cantidad_galletas = models.IntegerField()
    id_galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=False, related_name='lote_galleta_galleta')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, related_name='lote_galleta_usuario')
    
    def __str__(self):
        return f" {self.fecha_preparacion} - {self.estatus} - {self.cantidad_galletas} - {self.id_galleta} - {self.id_usuario}"
    
class Merma_producto(models.Model):
    id_merma = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=45)
    id_lote_galleta = models.ForeignKey(Lote_galleta, on_delete=models.CASCADE, null=False, related_name='merma_lote_galleta')
    def __str__(self):
        return f" {self.cantidad} - {self.motivo} - {self.id_lote_galleta}"