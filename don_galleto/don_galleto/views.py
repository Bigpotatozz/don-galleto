from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'
