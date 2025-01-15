from django.shortcuts import render, redirect
from .models import Chamado
import re

def formatar_whatsapp(numero):
    """
    Formata o número de WhatsApp no padrão (XX) XXXXX-XXXX.
    Aceita números com ou sem espaços, traços ou parênteses.
    """
    # Remove todos os caracteres que não sejam dígitos
    apenas_numeros = re.sub(r'\D', '', numero)

    # Verifica se o número tem 11 dígitos (padrão com DDD e 9 na frente)
    if len(apenas_numeros) == 11:
        return f"({apenas_numeros[:2]}) {apenas_numeros[2:7]}-{apenas_numeros[7:]}"
    elif len(apenas_numeros) == 10:  # Caso não tenha o 9 na frente
        return f"({apenas_numeros[:2]}) {apenas_numeros[2:6]}-{apenas_numeros[6:]}"
    else:
        raise ValueError("Número de WhatsApp inválido.")  # Gera erro para números com tamanho incorreto

def abrir_chamado(request):
    if request.method == "POST":
        try:
            # Obtenha os dados do formulário
            nome = request.POST.get('nome')
            sobrenome = request.POST.get('sobrenome')
            whatsapp = request.POST.get('whatsapp')
            email = request.POST.get('email')
            ramal = request.POST.get('ramal')
            numero_anydesk = request.POST.get('numero_anydesk')
            departamento = request.POST.get('departamento')
            tipo_problema = request.POST.get('tipo_problema')
            descricao_problema = request.POST.get('descricao_problema')
            urgencia = request.POST.get('urgencia')

            # Formata o número do WhatsApp
            whatsapp_formatado = formatar_whatsapp(whatsapp)

            # Salve o chamado no banco de dados
            chamado = Chamado.objects.create(
                nome=nome,
                sobrenome=sobrenome,
                whatsapp=whatsapp_formatado,  # Salva o número formatado
                email=email,
                ramal=ramal,
                numero_anydesk=numero_anydesk,
                departamento=departamento,
                tipo_problema=tipo_problema,
                descricao_problema=descricao_problema,
                urgencia=urgencia,
            )

            # Redirecione para uma página de confirmação ou lista de chamados
            return redirect('chamados:abrir_chamado')  # Substitua pela URL desejada

        except ValueError as e:
            # Retorna um erro de validação se o número for inválido
            return render(request, "abrir_chamado.html", {'error': str(e)})

    return render(request, "abrir_chamado.html")
