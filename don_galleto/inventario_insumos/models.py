from django.db import models
from proovedores.models import Proovedor


# Create your models here.
class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    tipo = models.CharField(max_length=45)
    tipo_medida = models.CharField(max_length=45)
    cantidad = models.IntegerField()
    estatus = models.CharField(max_length=45)
    
    def __str__(self):
        return f" {self.nombre} - {self.tipo} - {self.tipo_medida} - {self.cantidad} - {self.estatus}"
    
    
class Compra_insumo(models.Model):
    id_compra_insumo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    cantidad = models.FloatField()
    cantidad_restante = models.FloatField()
    caducidad = models.DateField()
    precio = models.FloatField()
    id_proovedor = models.ForeignKey(Proovedor, on_delete=models.CASCADE, null = False, related_name= 'compra_insumo_proovedor')
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null = False, related_name= 'compra_insumo_insumo')
    
    class Meta:
        db_table = 'compra_insumo'
    
    def __str__(self):
        return f" {self.nombre} - {self.cantidad} - {self.cantidad_restante} - {self.caducidad} - {self.precio} - {self.id_proovedor} - {self.id_insumo}"
    
class Merma_insumo(models.Model):
    id_merma_insumo = models.AutoField(primary_key=True)
    cantidad = models.FloatField()
    motivo = models.CharField(max_length=45)
    id_compra_insumo = models.ForeignKey(Compra_insumo, on_delete=models.CASCADE, null = False, related_name= 'merma_compra_insumo')
    
    class Meta: 
        db_table = 'merma_insumo'
    
    def __str__(self):
        return f" {self.cantidad} - {self.motivo} - {self.id_compra_insumo}"