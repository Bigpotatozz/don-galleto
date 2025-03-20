from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout

def dashboard(request):
    return render(request, 'dashboard.html')


    
        

