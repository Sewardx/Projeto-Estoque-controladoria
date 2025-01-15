from django.urls import path
from . import views

app_name = 'estoque'  # Define o namespace

urlpatterns = [
    path('', views.requisicao_material, name='requisicao_material'),  # Rota para o formulário de requisição de materiais
    path('api/materiais/', views.listar_materiais, name='api_materiais'),  # Rota para a API que lista os materiais
]
