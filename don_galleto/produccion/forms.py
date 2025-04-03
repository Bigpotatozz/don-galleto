from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Lote_galleta, Galleta, Merma_producto
from django.utils.timezone import now

class LoteGalletaForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.galleta  = kwargs.pop('galleta', None)
        #print(f"Request en __init__: {self.galleta}") 
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Validación si hay un lote en proceso
        if Lote_galleta.objects.filter(id_galleta=self.galleta).exclude(estatus__in=["Completado", "Caducado"]).exists():
            raise ValidationError(f"Ya hay un lote en proceso para la galleta {self.galleta.nombre}. No puedes crear otro hasta que se complete.")

        # Validación de stock suficiente
        if self.galleta.cantidad >= 100:
            raise ValidationError(f"Hay suficiente stock para crear un nuevo lote. En existencia: {self.galleta.cantidad} galletas disponibles.")

        # Validación si la receta tiene insumos asociados
        if not self.galleta.detalle_receta_galleta.exists():
            raise ValidationError("Esta receta no tiene insumos.")

        # Verificar si hay insumos suficientes
        insumos_faltantes = [
            f"{detalle.id_insumo.nombre} (Faltante: {detalle.cantidad - detalle.id_insumo.cantidad})"
            for detalle in self.galleta.detalle_receta_galleta.all()
            if detalle.id_insumo.cantidad < detalle.cantidad
        ]
        if insumos_faltantes:
            raise ValidationError(f"Insumos insuficientes: {', '.join(insumos_faltantes)}")

        return cleaned_data

    def guardar_lote_galleta(self, usuario):
        # Crear el lote si todas las validaciones son correctas
        lote = Lote_galleta.objects.create(
            cantidad_galletas=self.galleta.cantidad_receta,
            id_galleta=self.galleta,
            id_usuario=usuario,
            estatus="Pendiente",
            fecha_preparacion=now()
        )

        # Descontar los insumos
        for detalle_receta in self.galleta.detalle_receta_galleta.all():
            insumo = detalle_receta.id_insumo
            insumo.cantidad -= detalle_receta.cantidad
            insumo.save()

        return lote

class MermaRegistrarForm(forms.ModelForm):
    
    class Meta:
        model = Merma_producto
        fields = ['cantidad', 'motivo']
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ingrese la cantidad de merma"}),
            "motivo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese el motivo"}),
        }