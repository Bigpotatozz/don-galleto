from django.db import models

# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=60)
    contrasenia = models.CharField(max_length=45)
    rol = models.CharField(max_length=10, choices=[('empleado', 'empleado'), ('cliente', 'cliente')])
    codigo_verificacion = models.IntegerField()
    
    def __str__(self):
        return f" {self.nombre} - {self.telefono} - {self.correo} - {self.contrasenia} - {self.rol} - {self.codigo_verificacion}"