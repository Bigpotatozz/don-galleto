from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True, auto_created=True)
    telefono = models.CharField(max_length=10)
    rol = models.CharField(max_length=10, choices=[('empleado', 'empleado'), ('cliente', 'cliente'), ('admin', 'admin')], default='cliente')
    codigo_verificacion = models.IntegerField(blank=True, null=True)
    
    class Meta: 
        db_table = 'usuario'
        permissions = [("admin", "Control total"), 
                       ("empleado", "funcionalidades basicas"),
                       ("cliente", "acceso a la plataforma de compra")]
    
    def __str__(self):
        return f"{self.id_usuario} - {self.telefono} - {self.rol} - {self.codigo_verificacion}"
    
    
class Logs(models.Model):
    id_log = models.AutoField(primary_key= True, auto_created=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null = False, related_name= "logs")
    
    class Meta: 
        db_table = 'logs'