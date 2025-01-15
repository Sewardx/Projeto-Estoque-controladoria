from django.contrib import admin
from .models import Material, RequisicaoDeMaterial, RequisicaoDeMaterialItem, SolicitacaoCompra, SolicitacaoCompraItem


class RequisicaoDeMaterialItemInline(admin.TabularInline):
    model = RequisicaoDeMaterialItem
    extra = 1


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_produto','unidade', 'quantidade', 'fornecedor', 'descricao', 'codigo_produto')
    search_fields = ('nome', 'descricao', 'tipo_produto')


@admin.action(description="Aprovar requisições de materiais selecionadas")
def aprovar_requisicoes(modeladmin, request, queryset):
    for requisicao in queryset.filter(status="Pendente"):
        itens_aprovados = True

        for item in requisicao.itens.all():
            material = item.material
            if item.quantidade_solicitada > material.quantidade:
                modeladmin.message_user(
                    request,
                    f"Estoque insuficiente para {material.nome}. Requisição {requisicao.id} não foi aprovada.",
                    level="error",
                )
                itens_aprovados = False
                break

        if itens_aprovados:
            for item in requisicao.itens.all():
                material = item.material
                material.quantidade -= item.quantidade_solicitada
                material.save()
            requisicao.status = "Aprovado"
            requisicao.save()
            modeladmin.message_user(
                request,
                f"Requisição {requisicao.id} aprovada com sucesso.",
                level="success",
            )


@admin.action(description="Recusar requisições de materiais selecionadas")
def recusar_requisicoes(modeladmin, request, queryset):
    recusadas = queryset.filter(status="Pendente").update(status="Recusado")
    modeladmin.message_user(
        request,
        f"{recusadas} requisições foram recusadas.",
        level='warning'
    )

@admin.register(RequisicaoDeMaterial)
class RequisicaoDeMaterialAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'email', 'departamento', 'status', 'data_requisicao')
    list_filter = ('status', 'data_requisicao', 'departamento')
    search_fields = ('nome_completo', 'email', 'departamento')
    inlines = [RequisicaoDeMaterialItemInline]
    actions = [aprovar_requisicoes, recusar_requisicoes]


class SolicitacaoCompraItemInline(admin.TabularInline):
    model = SolicitacaoCompraItem
    extra = 1


@admin.action(description="Confirmar recebimento de compras selecionadas")
def aprovar_solicitacoes_compras(modeladmin, request, queryset):
    for solicitacao in queryset.filter(status="Pendente"):
        for item in solicitacao.itens.all():
            material = item.material
            material.quantidade += item.quantidade_comprada
            material.save()
        solicitacao.status = "Aprovado"
        solicitacao.save()
    modeladmin.message_user(request, "Solicitações de compras aprovadas com sucesso!")


@admin.register(SolicitacaoCompra)
class SolicitacaoCompraAdmin(admin.ModelAdmin):
    list_display = ('fornecedor', 'status', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('fornecedor',)
    inlines = [SolicitacaoCompraItemInline]
    actions = [aprovar_solicitacoes_compras]

