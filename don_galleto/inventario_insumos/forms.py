from django import forms
from inventario_insumos.models import Insumo
from proovedores.models import Proovedor
from inventario_insumos.models import Compra_insumo, Merma_insumo
from django.utils.timezone import now
from django.contrib.auth import get_user_model

class Registro_insumo_form(forms.ModelForm):
    nombre = forms.CharField(max_length=45)
    tipo = forms.ChoiceField(choices=[('base', 'Base'), ('complemento', 'Complemento')])
    tipo_medida = forms.ChoiceField(choices=[('g', 'gramos'), ('ml', 'mililitros')])
    
    class Meta:
        model = Insumo
        fields = ['nombre', 'tipo', 'tipo_medida']
        
    def save(self):
        nombre = self.cleaned_data['nombre']
        tipo = self.cleaned_data['tipo']
        tipo_medida = self.cleaned_data['tipo_medida']
        
        new_insumo = Insumo(nombre=nombre, tipo=tipo, tipo_medida=tipo_medida, cantidad = 0, estatus = 'sin existencias')
        new_insumo.save()

class Registro_compra_insumo_form(forms.ModelForm):
    nombre = forms.CharField(max_length=45)
    cantidad = forms.FloatField()
    caducidad = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    

    id_proovedor_id = forms.ModelChoiceField(
        queryset = Proovedor.objects.all(),
        label = "proovedor",
        to_field_name = "id_proovedor"
    )

    id_insumo_id = forms.ModelChoiceField(
        queryset = Insumo.objects.all(),
        label = "Insumo",
        to_field_name = "id_insumo"
    )

    class Meta:
        model = Compra_insumo
        fields = ['nombre', 'cantidad','caducidad', 'total','id_proovedor_id', 'id_insumo_id']

    def save(self, commit = True):
        nombre = self.cleaned_data['nombre']
        cantidad = self.cleaned_data['cantidad']
        caducidad = self.cleaned_data['caducidad']
        total = self.cleaned_data['total']
        id_proovedor_id = self.cleaned_data['id_proovedor_id'].id_proovedor
        id_insumo_id = self.cleaned_data['id_insumo_id'].id_insumo
        precio_unitario = total / cantidad
        
        
        new_compra_insumo = Compra_insumo(nombre = nombre, 
                                          cantidad = cantidad, 
                                          cantidad_restante = cantidad,
                                          caducidad = caducidad, 
                                          total = total,
                                          precio_unitario = precio_unitario,
                                          estatus = "disponible",
                                          id_proovedor_id = id_proovedor_id, 
                                          id_insumo_id = id_insumo_id)

        insumo = Insumo.objects.get(id_insumo = id_insumo_id)
        insumo.cantidad = insumo.cantidad + cantidad
        insumo.estatus = "disponible"
        insumo.precio_unitario = precio_unitario

        

        if commit: 
            new_compra_insumo.save()
            insumo.save()
            
class Registro_merma_insumo_form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        # Extrae explícitamente el request
        self.request = kwargs.pop('request', None)
        print(f"Request en __init__: {self.request}")  # Depuración
        super().__init__(*args, **kwargs)
    
    cantidad = forms.FloatField()
    motivo = forms.CharField(max_length=45)
    
    id_insumo = forms.ModelChoiceField(
        queryset = Insumo.objects.filter(estatus = "disponible"),
        label = "Insumo",
        to_field_name = "id_insumo"
    )
    
    
    class Meta: 
        model = Merma_insumo
        fields = ['cantidad', 'motivo', 'id_insumo' ]
    
    def save(self, commit = True):
        cantidad = self.cleaned_data['cantidad']        
        motivo = self.cleaned_data['motivo']
        id_insumo = self.cleaned_data['id_insumo'].id_insumo
        compra_insumo = Compra_insumo.objects.filter(caducidad__gte = now().date(), id_insumo = id_insumo, estatus = "disponible").order_by('caducidad').first()
        insumo = Insumo.objects.get(id_insumo = id_insumo)
            
        merma_insumo =  Merma_insumo(cantidad = cantidad,
                                     motivo = motivo,
                                     id_compra_insumo_id = compra_insumo.id_compra_insumo,
                                     fecha = now().date(),
                                     id_usuario_id = self.request.id_usuario)
        compra_insumo.cantidad_restante -= cantidad
        
        if(cantidad > insumo.cantidad):
            raise forms.ValidationError('No hay suficientes insumos')
        else: 
            insumo.cantidad -= cantidad
        
        if commit:
            merma_insumo.save()
            compra_insumo.save()
            insumo.save()