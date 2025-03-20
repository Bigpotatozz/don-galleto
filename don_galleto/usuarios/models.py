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
        return f" {self.nombre} - {self.telefono} - {self.correo} - {self.contrasenia} - {self.rol} - {self.codigo_verificacion}"