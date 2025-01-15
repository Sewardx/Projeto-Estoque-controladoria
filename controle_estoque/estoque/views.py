from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.core.cache import cache
from .models import Material, RequisicaoDeMaterial, RequisicaoDeMaterialItem
import json
import logging

logger = logging.getLogger(__name__)

def requisicao_material(request):
    if request.method == "POST":
        try:
            # Captura os campos do formulário
            nome_completo = request.POST.get("nome_completo", "Usuário Desconhecido")
            email = request.POST.get("email", "")
            departamento = request.POST.get("departamento", "Não informado")

            materials_json = request.POST.get("materials", "[]")
            quantidades_json = request.POST.get("quantidades", "[]")

            try:
                materials = json.loads(materials_json)
                quantidades = json.loads(quantidades_json)
            except json.JSONDecodeError:
                messages.error(request, "Erro ao processar os dados enviados.")
                return redirect("estoque:requisicao_material")

            if not materials or not quantidades or len(materials) != len(quantidades):
                messages.error(request, "Dados de materiais ou quantidades estão incompletos.")
                return redirect("estoque:requisicao_material")

            # Cria a requisição sem alterar o estoque
            with transaction.atomic():
                requisicao = RequisicaoDeMaterial.objects.create(
                    nome_completo=nome_completo,
                    email=email,
                    departamento=departamento,
                )

                for material_id, quantidade in zip(materials, quantidades):
                    try:
                        material = Material.objects.get(id=material_id)
                        quantidade = int(quantidade)

                        if quantidade > material.quantidade:
                            messages.error(
                                request,
                                f"Estoque insuficiente para {material.nome}. Disponível: {material.quantidade}."
                            )
                            raise ValueError("Estoque insuficiente")

                        # Apenas registra o item na requisição
                        RequisicaoDeMaterialItem.objects.create(
                            requisicao=requisicao,
                            material=material,
                            quantidade_solicitada=quantidade,
                        )
                    except Material.DoesNotExist:
                        messages.error(request, f"Material com ID {material_id} não encontrado.")
                        raise

            messages.success(request, "Requisição enviada com sucesso! Aguardando aprovação.")
            return redirect("estoque:requisicao_material")

        except Exception as e:
            logger.error(f"Erro ao processar requisição: {str(e)}")
            messages.error(request, "Erro ao processar a requisição. Tente novamente.")
            return redirect("estoque:requisicao_material")

    materials = Material.objects.filter(quantidade__gt=0)
    return render(request, "estoque/estoque_controladoria.html", {"materials": materials})

def listar_materiais(request):
    materiais = cache.get('materiais')
    if not materiais:
        # Filtro para trazer apenas materiais com quantidade maior que zero
        materiais = list(Material.objects.filter(quantidade__gt=0).values('id', 'nome', 'quantidade', 'tipo_produto', 'unidade'))
        cache.set('materiais', materiais, 60 * 15)  # Cache por 15 minutos
    return JsonResponse(materiais, safe=False)

from django.shortcuts import get_object_or_404

def aprovar_requisicao(request, requisicao_id):
    requisicao = get_object_or_404(RequisicaoDeMaterial, id=requisicao_id)
    if requisicao.status != 'Pendente':
        messages.warning(request, "Essa requisição já foi processada.")
        return redirect("admin:estoque_requisicaodematerial_changelist")

    with transaction.atomic():
        for item in requisicao.itens.select_for_update():
            if item.quantidade_solicitada > item.material.quantidade:
                messages.error(
                    request,
                    f"Estoque insuficiente para {item.material.nome}. Disponível: {item.material.quantidade}."
                )
                requisicao.status = 'Recusado'
                requisicao.save()
                return redirect("admin:estoque_requisicaodematerial_changelist")

            # Atualiza o estoque
            item.material.quantidade -= item.quantidade_solicitada
            item.material.save()

        requisicao.status = 'Aprovado'
        requisicao.save()

    messages.success(request, "Requisição aprovada com sucesso!")
    return redirect("admin:estoque_requisicaodematerial_changelist")
