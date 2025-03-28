from django.db import models
from inventario_insumos.models import Insumo
from django.core.validators import MinValueValidator

# Create your models here.
class Galleta(models.Model):
    id_galleta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
<<<<<<< HEAD
    precio_venta = models.FloatField()
    cantidad = models.IntegerField(default=0)
    cantidad_receta = models.IntegerField()
    peso_unidad = models.FloatField()
    duracion_promedio = models.IntegerField()
=======
    costo = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    precio_venta = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    cantidad_por_lote = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    peso_unidad = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    duracion_promedio = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
>>>>>>> 41544858cbbcb5a5c4e98f3b02f1186925d54593
    
    class Meta: 
        db_table = 'galleta'
    
    def __str__(self):
           return f" {self.nombre} - {self.descripcion} - {self.precio_venta} - {self.cantidad} - {self.peso_unidad} - {self.duracion_promedio}"
    
class Detalle_receta(models.Model):
    id_detalle_receta = models.AutoField(primary_key=True)
    cantidad = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=False, related_name='detalle_receta_insumo')
    id_galleta = models.ForeignKey(Galleta, on_delete=models.CASCADE, null=False, related_name='detalle_receta_galleta')
    
    class Meta:
        db_table = 'detalle_receta'
    
    def __str__(self):
        return f" {self.cantidad} - {self.id_insumo} - {self.id_galleta}"