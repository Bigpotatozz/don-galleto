from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from don_galleto.forms import RegistroForm
from django.contrib.auth import login
from django.contrib.auth.models import Group

class IndexView(TemplateView):
    template_name = 'index.html'

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request,"registration/registro.html",{"form":form})