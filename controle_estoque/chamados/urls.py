from django.urls import path
from . import views

app_name = 'chamados'  # Define o namespace

urlpatterns = [
    path('', views.abrir_chamado, name='abrir_chamado'),
]
