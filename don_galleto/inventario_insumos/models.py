from django.db import models
from proovedores.models import Proovedor
from usuarios.models import Usuario
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.
class Insumo(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    tipo = models.CharField(max_length=45)
    tipo_medida = models.CharField(max_length=45)
    cantidad = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    precio_unitario = models.FloatField(default = 0,
                                        validators=[MinValueValidator(0)])
    estatus = models.CharField(max_length=45)
    
    class Meta:
        db_table = 'insumo'
    
    def __str__(self):
        return f" {self.nombre} - {self.tipo} - {self.tipo_medida} - {self.cantidad} - {self.estatus}"
    
    
class Compra_insumo(models.Model):
    id_compra_insumo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    cantidad = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    cantidad_restante = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    caducidad = models.DateField(
        validators=[MinValueValidator(timezone.now().date())]
    )
    total = models.FloatField(default=0,
                              validators=[MinValueValidator(0)])
    precio_unitario = models.FloatField(default = 0,
                                        validators=[MinValueValidator(0)])
    estatus = models.CharField(max_length=15, default = "")
    fecha_registro = models.DateField(auto_now_add=True)
    id_proovedor = models.ForeignKey(Proovedor, on_delete=models.CASCADE, null = False, related_name= 'compra_insumo_proovedor')
    id_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null = False, related_name= 'compra_insumo_insumo')
    
    class Meta:
        db_table = 'compra_insumo'
    
    def __str__(self):
        return f" {self.nombre} - {self.cantidad} - {self.cantidad_restante} - {self.caducidad} - {self.precio} - {self.id_proovedor} - {self.id_insumo}"
    
class Merma_insumo(models.Model):
    id_merma_insumo = models.AutoField(primary_key=True)
    cantidad = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    motivo = models.CharField(max_length=45)
    fecha = models.DateField(null=True)
    id_compra_insumo = models.ForeignKey(Compra_insumo, on_delete=models.CASCADE, null = False, related_name= 'merma_compra_insumo')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null= False, related_name='merma_insumo_usuario')
    
    class Meta: 
        db_table = 'merma_insumo'
    
    def __str__(self):
        return f" {self.cantidad} - {self.motivo} - {self.id_compra_insumo}"