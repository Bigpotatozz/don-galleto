from django.db import models

class Proovedor(models.Model):
    id_proovedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    nombre_contacto = models.CharField(max_length=30)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(max_length=45)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=15),
    estado = models.CharField(max_length=15)
    codigo_postal = models.CharField(max_length=7)
    estatus = models.CharField(max_length=10, default = 'activo')
    
    def __str__(self):
        return f" {self.nombre} - {self.nombre_contacto} - {self.telefono} - {self.correo} - {self.direccion} - {self.ciudad} - {self.estado} - {self.codigo_postal} - {self.estatus}"

