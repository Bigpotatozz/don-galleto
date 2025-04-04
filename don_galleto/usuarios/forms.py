from django import forms
from django.shortcuts import redirect
from usuarios.models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

class Registro_admin_form(UserCreationForm):
        
        telefono = forms.CharField(max_length=10)
        rol = forms.ChoiceField(choices=[('empleado', 'Empleado'), ('cliente', 'Cliente'), ('admin', 'admin')])
        
        class Meta: 
            model = Usuario
            fields = ['username', 'email', 'password1', 'password2', 'telefono', 'rol']
            
            
            

class Edicion_usuario_form(forms.ModelForm):
      
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    contrasenia = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)
    telefono = forms.CharField(max_length=10)
    rol = forms.ChoiceField(choices=[('empleado', 'Empleado'), ('cliente', 'Cliente'), ('admin', 'admin')])
    is_active = forms.BooleanField(required=False, initial=True)


    class Meta:
          model = Usuario
          fields = ['username', 'email', 'contrasenia', 'telefono', 'rol', 'is_active']

    def save(self, id):
        
        usuario = Usuario.objects.get(id_usuario=id)
        usuario.username = self.cleaned_data['username']
        usuario.email = self.cleaned_data['email']
        usuario.telefono = self.cleaned_data['telefono']
        usuario.rol = self.cleaned_data['rol']
        nueva_contrasena = self.cleaned_data.get('contrasenia')
        usuario.is_active = self.cleaned_data['is_active']

        if nueva_contrasena:
             usuario.set_password(nueva_contrasena)
        
        usuario.save()
        return usuario


class Login_form(forms.Form):
    
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    captcha = ReCaptchaField()
        
    def auth(self):                                         
        usuario = self.cleaned_data['username']
        contrasenia = self.cleaned_data['password']
        
        user_auth = authenticate(username=usuario, password=contrasenia)
        
        print(user_auth)
        
        if user_auth is not None:   
            
            return user_auth
        return None 
        
        
class Verification_form(forms.Form):
    codigo = forms.IntegerField(
        label="Código de verificación",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el código de 4 dígitos',
            'autocomplete': 'off',
            'inputmode': 'numeric'
        }),
        min_value=1000,
        max_value=9999,
        error_messages={
            'required': 'Por favor ingrese el código de verificación',
            'invalid': 'Debe ser un número entre 1000 y 9999',
            'min_value': 'El código debe tener 4 dígitos',
            'max_value': 'El código debe tener 4 dígitos'
        }
    )
        
    def verificar_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        
        try:
            usuario = Usuario.objects.get(codigo_verificacion=codigo)
            usuario.codigo_verificacion = None
            usuario.save()
            
            return usuario
            
        except Usuario.DoesNotExist:
            raise ValidationError(
                "Código incorrecto o expirado",
                code='invalid_code'
            )
        except MultipleObjectsReturned:
            raise ValidationError(
                "Error aiuda",
                code='system_error'
            )
        