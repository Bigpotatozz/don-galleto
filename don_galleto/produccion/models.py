from django.db import models
from galletas.models import Galleta
from usuarios.models import Usuario
from django.core.validators import MinValueValidator
from datetime import timedelta
from django.utils.timezone import now


# Create your models here.
class Lote_galleta(models.Model):
    ESTATUS_OPCIONES = [
        ('Pendiente', 'Pendiente'),
        ('Mezclando', 'Mezclando'),
        ('Formando', 'Formando'),
        ('Horneando', 'Horneando'),
        ('Enfriando', 'Enfriando'),
        ('Completado', 'Completado'),
        ('Caducado', 'Caducado'),
    ]

    id_lote_galleta = models.AutoField(primary_key=True)
    fecha_preparacion = models.DateField()
    estatus = models.CharField(max_length=45, choices=ESTATUS_OPCIONES, default='Pendiente')
    cantidad_galletas = models.IntegerField(
        validators=[MinValueValidator(1)],
    )
    caducidad_lote = models.DateField(null=True, blank=True)
    id_galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, related_name='lote_galleta_galleta')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='lote_galleta_usuario')
    
    def save(self, *args, **kwargs):
        if not self.caducidad_lote and self.id_galleta.duracion_promedio:
            self.caducidad_lote = self.fecha_preparacion + timedelta(days=self.id_galleta.duracion_promedio)
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'lote_galleta'
        ordering = ['-id_lote_galleta']

    def __str__(self):
        return f"Lote {self.id_lote_galleta} - {self.fecha_preparacion} - {self.get_estatus_display()} - {self.cantidad_galletas} - {self.id_galleta.nombre}"



class Merma_producto(models.Model):
    id_merma = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)],
    )
    motivo = models.CharField(max_length=45)
    id_lote_galleta = models.ForeignKey(Lote_galleta, on_delete=models.CASCADE, null=False, related_name='merma_lote_galleta')
    
    class Meta:
        db_table = 'merma_producto'
    def __str__(self):
        return f" {self.cantidad} - {self.motivo} - {self.id_lote_galleta}"
    
    