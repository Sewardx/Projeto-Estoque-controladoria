from django.contrib import admin
from .models import Chamado

@admin.action(description="Marcar chamados como atendidos")
def marcar_como_atendido(modeladmin, request, queryset):
    queryset.update(status='Atendido')
    modeladmin.message_user(request, "Chamados marcados como atendidos.")

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'departamento', 'tipo_problema', 'urgencia', 'status', 'data_solicitacao')
    list_filter = ('status', 'urgencia', 'departamento')
    search_fields = ('nome', 'sobrenome', 'tipo_problema', 'descricao_problema')
    actions = [marcar_como_atendido]
