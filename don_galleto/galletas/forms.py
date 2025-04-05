from django import forms
from inventario_insumos.models import Insumo
from proovedores.models import Proovedor
from galletas.models import Galleta, Detalle_receta
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.validators import MinValueValidator

class Registro_galleta_form(forms.ModelForm):
    nombre = forms.CharField(max_length=30)
    descripcion = forms.CharField(max_length=100)
<<<<<<< HEAD
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
=======
    peso_unidad = forms.FloatField(validators=[MinValueValidator(1)])
    duracion_promedio = forms.IntegerField(validators=[MinValueValidator(1)])
    cantidad_receta = forms.IntegerField(validators=[MinValueValidator(1)])
    precio_venta = forms.FloatField(validators=[MinValueValidator(1)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        insumos = Insumo.objects.all()
        
        for insumo in insumos:
>>>>>>> e33470e3ee6a8f4f36910eb9b4fe75097097f26a
    
            self.fields[f'insumo_{insumo.id_insumo}'] = forms.IntegerField(
                label=insumo.nombre,
                required=False, 
                widget=forms.NumberInput(attrs={'placeholder': 'Cantidad de insumo'}),
                initial = 0
            )

    class Meta:
        model = Galleta
        fields = [
            'nombre', 
            'descripcion', 
            'peso_unidad', 
            'duracion_promedio', 
            'precio_venta'
        ]
    
    def save(self, commit=True):
        nombre = self.cleaned_data['nombre']
        descripcion = self.cleaned_data['descripcion']
        peso_unidad = self.cleaned_data['peso_unidad']
        duracion_promedio = self.cleaned_data['duracion_promedio']
        cantidad_receta = self.cleaned_data['cantidad_receta']
        precio_venta = self.cleaned_data['precio_venta']

        with transaction.atomic():
            galleta = Galleta(
                nombre=nombre,
                descripcion=descripcion,
                precio_venta=precio_venta,
                cantidad=0,  
                cantidad_receta=cantidad_receta,
                peso_unidad=peso_unidad,
                duracion_promedio=duracion_promedio,
                costo=0  
            )
            galleta.save()

            for insumo in Insumo.objects.all():  
                field_name = f'insumo_{insumo.id_insumo}'  
                cantidad = self.cleaned_data.get(field_name, 0)

                if cantidad > 0:
                    detalle = Detalle_receta(
                        cantidad=cantidad,
                        id_insumo_id=insumo.id_insumo,
                        id_galleta_id=galleta.id_galleta
                    )
                    detalle.save()

        return galleta

class Editar_galleta_form(forms.ModelForm):
    nombre = forms.CharField(max_length=30)
    descripcion = forms.CharField(max_length=100)
    peso_unidad = forms.FloatField(validators=[MinValueValidator(1)])
    duracion_promedio = forms.IntegerField(validators=[MinValueValidator(1)])
    cantidad_receta = forms.IntegerField(validators=[MinValueValidator(1)])
    precio_venta = forms.FloatField(validators=[MinValueValidator(1)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        insumos = Insumo.objects.all()
        
        for insumo in insumos:
    
            self.fields[f'insumo_{insumo.id_insumo}'] = forms.IntegerField(
                label=insumo.nombre,
                required=False, 
                widget=forms.NumberInput(attrs={'placeholder': 'Cantidad de insumo'}),
                initial = 0
            )

    class Meta:
        model = Galleta
        fields = [
            'nombre', 
            'descripcion', 
            'peso_unidad', 
            'duracion_promedio', 
            'precio_venta'
        ]
    
    def save(self, id):
        
        
        nombre = self.cleaned_data['nombre']
        descripcion = self.cleaned_data['descripcion']
        peso_unidad = self.cleaned_data['peso_unidad']
        imagen = self.cleaned_data['imagen']
        duracion_promedio = self.cleaned_data['duracion_promedio']
        cantidad_receta = self.cleaned_data['cantidad_receta']
        precio_venta = self.cleaned_data['precio_venta']

        with transaction.atomic():
<<<<<<< HEAD
            
            galleta = Galleta(nombre = nombre,
                              descripcion = descripcion,
                              precio_venta = 0,
                              cantidad = 0,
                              cantidad_receta = cantidad_receta,
                              peso_unidad = peso_unidad,
                              imagen = imagen,
                              duracion_promedio = duracion_promedio,
                              costo = 0)
=======
>>>>>>> e33470e3ee6a8f4f36910eb9b4fe75097097f26a

            galleta = Galleta.objects.get(id_galleta = id);
            galleta.nombre = nombre
            galleta.descripcion = descripcion
            galleta.peso_unidad = peso_unidad
            galleta.duracion_promedio = duracion_promedio
            galleta.cantidad_receta = cantidad_receta
            galleta.precio_venta = precio_venta
            galleta.save()

            for insumo in Insumo.objects.all():  
                field_name = f'insumo_{insumo.id_insumo}'  
                cantidad = self.cleaned_data.get(field_name, 0)
                 # Buscar el detalle existente
                detalle = Detalle_receta.objects.filter(
                    id_insumo=insumo,
                    id_galleta=galleta
                ).first()
                
                if cantidad > 0:
                    
                    if detalle:
                        detalle.cantidad = cantidad
                        detalle.save()
                    else:
                        Detalle_receta.objects.create(
                            id_insumo=insumo,
                            id_galleta=galleta,
                            cantidad=cantidad
                        )
                elif detalle:
                    
                    detalle.delete()
        return galleta