from inventario_insumos.models import Insumo
from django.db import connection

def verificar_insumos():
    with connection.cursor() as stored_procedure:
       stored_procedure.callproc('actualizar_caducidad_insumos')
    
    
