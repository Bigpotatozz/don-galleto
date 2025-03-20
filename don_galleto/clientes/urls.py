from django.urls import path
from . import views
from clientes.views import dashboard

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]