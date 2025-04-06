from django.contrib.auth.models import Group,  Permission
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Logs
from datetime import date
from django.contrib.auth.models import Permission


def asignar_permisos(form, id: int | None):

    if(id):
        user = form.save(id)
    else:
        user = form.save()
    
        
    
    if user.rol == "cliente":
        grupo, created = Group.objects.get_or_create(name="cliente")
        user.groups.add(grupo)
        user.save()
        return redirect('listado_usuarios')
    elif user.rol == "admin":
        grupo, created = Group.objects.get_or_create(name="admin")
        user.groups.add(grupo)
        user.save()
        return redirect('listado_usuarios')
    elif user.rol == "empleado":
        grupo, created = Group.objects.get_or_create(name="empleado")
        user.groups.add(grupo)
        user.save()
        return redirect('listado_usuarios')
    
    
def log(self, form, titulo):
    
    if self.request.user.is_authenticated:
            Logs.objects.create(
                fecha = date.today(),
                tipo = f"{titulo}",
                descripcion = f"{titulo}",
                id_usuario = self.request.user
            )
    
