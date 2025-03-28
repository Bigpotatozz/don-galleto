from django import forms
<<<<<<< HEAD
from .models import Galleta, Detalle_receta

class GalletaForm(forms.ModelForm):
    class Meta:
        model = Galleta
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_receta', 'peso_unidad', 'duracion_promedio']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la galleta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la galleta'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de venta'}),
            'cantidad_receta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en receta'}),
            'peso_unidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso por unidad (g)'}),
            'duracion_promedio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración promedio (días)'}),
        }
class DetalleRecetaForm(forms.ModelForm):
    class Meta:
        model = Detalle_receta
        fields = ['id_insumo', 'cantidad']
        
        widgets = {
            'id_insumo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad del insumo'}),
        }

class GalletaEditarForm(forms.ModelForm):
    class Meta:
        model = Galleta
        fields = ['nombre', 'descripcion', 'precio_venta', 'cantidad_receta', 'peso_unidad', 'duracion_promedio']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la galleta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la galleta'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio de venta'}),
            'cantidad_receta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad en receta'}),
            'peso_unidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso por unidad (g)'}),
            'duracion_promedio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración promedio (días)'}),
        }
        
    def save(self, id):
        galleta = Galleta.objects.filter(id_galleta=id).first()
        galleta.nombre = self.cleaned_data['nombre']
        galleta.descripcion = self.cleaned_data['descripcion']
        galleta.precio_venta = self.cleaned_data['precio_venta']
        galleta.cantidad_receta = self.cleaned_data['cantidad_receta']
        galleta.peso_unidad = self.cleaned_data['peso_unidad']
        galleta.duracion_promedio = self.cleaned_data['duracion_promedio']
        galleta.save()        

=======
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
    duracion_promedio = forms.IntegerField()
    cantidad_por_lote = forms.IntegerField()
    
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
        duracion_promedio = self.cleaned_data['duracion_promedio']
        cantidad_por_lote = self.cleaned_data['cantidad_por_lote']
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
                              cantidad_por_lote = cantidad_por_lote,
                              peso_unidad = peso_unidad,
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
            segunda_request.costo = costo / cantidad_por_lote
            segunda_request.precio_venta = costo / cantidad_por_lote * 2
            
            
            segunda_request.save()



        
   
    
>>>>>>> 41544858cbbcb5a5c4e98f3b02f1186925d54593
