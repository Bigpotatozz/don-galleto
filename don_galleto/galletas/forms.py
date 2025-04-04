from django import forms
from inventario_insumos.models import Insumo
from proovedores.models import Proovedor
from galletas.models import Galleta, Detalle_receta
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db import transaction

class Registro_galleta_form(forms.ModelForm):
    
    nombre = forms.CharField(max_length=30)
    descripcion = forms.CharField(max_length=100)
    peso_unidad = forms.FloatField()
    imagen = forms.ImageField(required=False)
    duracion_promedio = forms.IntegerField()
    cantidad_receta = forms.IntegerField()
    
    ingrediente1 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad1 = forms.FloatField()
    
    ingrediente2 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad2 = forms.FloatField()
    ingrediente3 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad3 = forms.FloatField()
    ingrediente4 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad4 = forms.FloatField()
    ingrediente5 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad5 = forms.FloatField()
    ingrediente6 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad6 = forms.FloatField()
    ingrediente7 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad7 = forms.FloatField()
    ingrediente8 = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = 'disponible'),
        label = "Ingrediente",
        to_field_name = "id_insumo"
    )
    cantidad8 = forms.FloatField()
    
    class Meta:
        model = Galleta
        fields = [
            'nombre', 
            'descripcion', 
            'peso_unidad', 
            'duracion_promedio', 
            'ingrediente1', 
            'ingrediente2', 
            'ingrediente3', 
            'ingrediente4', 
            'ingrediente5', 
            'ingrediente6', 
            'ingrediente7', 
            'ingrediente8',
            'cantidad1',
            'cantidad2',
            'cantidad3',
            'cantidad4',
            'cantidad5',
            'cantidad6',
            'cantidad7',
            'cantidad8',
        ]
    
    def save(self, commit = True):
        
        nombre = self.cleaned_data['nombre']
        descripcion = self.cleaned_data['descripcion']
        peso_unidad = self.cleaned_data['peso_unidad']
        imagen = self.cleaned_data['imagen']
        duracion_promedio = self.cleaned_data['duracion_promedio']
        cantidad_receta = self.cleaned_data['cantidad_receta']
        ingredientes = [self.cleaned_data['ingrediente1'],
                        self.cleaned_data['ingrediente2'],
                        self.cleaned_data['ingrediente3'],
                        self.cleaned_data['ingrediente4'],
                        self.cleaned_data['ingrediente5'],
                        self.cleaned_data['ingrediente6'],
                        self.cleaned_data['ingrediente7'],
                        self.cleaned_data['ingrediente8']]
        
        cantidades = [self.cleaned_data['cantidad1'],
                      self.cleaned_data['cantidad2'],
                      self.cleaned_data['cantidad3'],
                      self.cleaned_data['cantidad4'],
                      self.cleaned_data['cantidad5'],
                      self.cleaned_data['cantidad6'],
                      self.cleaned_data['cantidad7'],
                      self.cleaned_data['cantidad8']]
        
        with transaction.atomic():
            
            galleta = Galleta(nombre = nombre,
                              descripcion = descripcion,
                              precio_venta = 0,
                              cantidad = 0,
                              cantidad_receta = cantidad_receta,
                              peso_unidad = peso_unidad,
                              imagen = imagen,
                              duracion_promedio = duracion_promedio,
                              costo = 0)

            galleta.save()
            
            id_galleta =  galleta.id_galleta
            
            costo = 0
            contador = 0
            for ingrediente in ingredientes:
                detalle_receta = Detalle_receta(cantidad = cantidades[contador], id_insumo = ingrediente, id_galleta = galleta)
                detalle_receta.save()
                insumo = Insumo.objects.get(id_insumo = ingrediente.id_insumo)
                subtotal = insumo.precio_unitario * cantidades[contador]
                costo += subtotal
                contador += 1
        
            segunda_request = Galleta.objects.get(id_galleta = id_galleta)
            segunda_request.costo = costo / cantidad_receta
            segunda_request.precio_venta = costo / cantidad_receta * 2
            
            
            segunda_request.save()



        
   
    