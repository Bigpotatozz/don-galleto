from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario

class RegistroForm(UserCreationForm):
    
    telefono = forms.CharField(max_length=10)
    
    class Meta: 
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'telefono']


