from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout

class Registro_view(FormView):
    template_name = 'registro.html'
    form_class = forms.Form_registrar_usuario
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class Login_view(FormView):
    template_name = 'login.html'
    form_class = forms.Form_iniciar_sesion
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.auth()
        if user:
            
            self.request.session['id_usuario'] = user.id_usuario
            return super().form_valid(form)
        else:
            form.add_error(None, "Credenciales inválidas")
            return self.form_invalid(form)
        
def logout_view(request):
    
    if('user_id' in request.session):
        del request.session['user_id']
        
    logout(request)
    return redirect('home')
    