from django import forms
from inventario_insumos.models import Insumo
from proovedores.models import Proovedor
from inventario_insumos.models import Compra_insumo

class Registro_insumo_form(forms.ModelForm):
    nombre = forms.CharField(max_length=45)
    tipo = forms.ChoiceField(choices=[('base', 'Base'), ('complemento', 'Complemento')])
    tipo_medida = forms.ChoiceField(choices=[('gramos', 'Gramos'), ('mililitros', 'Mililitros')])
    
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
    precio = forms.FloatField()

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
        fields = ['nombre', 'cantidad','caducidad', 'precio', 'id_proovedor_id', 'id_insumo_id']

    def save(self, commit = True):
        nombre = self.cleaned_data['nombre']
        cantidad = self.cleaned_data['cantidad']
        caducidad = self.cleaned_data['caducidad']
        precio = self.cleaned_data['precio']
        id_proovedor_id = self.cleaned_data['id_proovedor_id'].id_proovedor
        id_insumo_id = self.cleaned_data['id_insumo_id'].id_insumo
        new_compra_insumo = Compra_insumo(nombre = nombre, 
                                          cantidad = cantidad, 
                                          cantidad_restante = 0,
                                          caducidad = caducidad, 
                                          precio = precio, 
                                          id_proovedor_id = id_proovedor_id, 
                                          id_insumo_id = id_insumo_id)

        
        insumo = Insumo.objects.get(id_insumo = id_insumo_id)
        insumo.cantidad = insumo.cantidad + cantidad

        

        if commit: 
            new_compra_insumo.save()
            insumo.save()