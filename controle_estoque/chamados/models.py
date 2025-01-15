from django.db import models

class Chamado(models.Model):
    URGENCIAS = [
        ('Nível diretoria', 'Nível diretoria'),
        ('Consigo trabalhar, porém o programa não funciona', 'Consigo trabalhar, porém o programa não funciona'),
        ('Não consigo trabalhar, nada funciona', 'Não consigo trabalhar, nada funciona'),
        ('Não consigo trabalhar, meu computador não funciona', 'Não consigo trabalhar, meu computador não funciona'),
        ('Consigo trabalhar, porém o computador trava muito', 'Consigo trabalhar, porém o computador trava muito'),
        ('Consigo esperar algum tempo', 'Consigo esperar algum tempo'),
        ('Posso esperar 30 minutos', 'Posso esperar 30 minutos'),
        ('Posso esperar 1 hora', 'Posso esperar 1 hora'),
        ('Posso esperar 3 horas', 'Posso esperar 3 horas'),
        ('Posso esperar 1 dia', 'Posso esperar 1 dia'),
        ('Estou sem pressa, porém precisa ser resolvido', 'Estou sem pressa, porém precisa ser resolvido'),
        ('Precisa ser resolvido até o final do dia', 'Precisa ser resolvido até o final do dia'),
        ('Precisa ser resolvido na próxima semana', 'Precisa ser resolvido na próxima semana'),
    ]

    TIPOS_PROBLEMA = [
        ('Problemas técnicos no computador', 'Problemas técnicos no computador'),
        ('Computador quebrado', 'Computador quebrado'),
        ('Problemas relacionados ao Protheus (TOTVS)', 'Problemas relacionados ao Protheus (TOTVS)'),
        ('Perda de internet', 'Perda de internet'),
        ('Problemas de Rede', 'Problemas de Rede'),
        ('Erro em Sistema ou Software', 'Erro em Sistema ou Software'),
        ('Outro', 'Outro'),
    ]

    DEPARTAMENTOS = [
        ('Tecnologia', 'Tecnologia'),
        ('Recepção', 'Recepção'),
        ('Diretoria', 'Diretoria'),
        ('Departamento Pessoal', 'Departamento Pessoal'),
        ('Financeiro', 'Financeiro'),
        ('Contabilidade', 'Contabilidade'),
        ('Contratos', 'Contratos'),
        ('Consórcios', 'Consórcios'),
        ('Controladoria', 'Controladoria'),
        ('Jurídico', 'Jurídico'),
        ('Licitação', 'Licitação'),
        ('Segurança do Trabalho', 'Segurança do Trabalho'),
        ('Obras', 'Obras'),
        ('Equipes', 'Equipes'),
    ]

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15)
    email = models.EmailField()
    ramal = models.CharField(max_length=10, blank=True, null=True)
    numero_anydesk = models.CharField(max_length=15, blank=True, null=True)
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTOS)
    tipo_problema = models.CharField(max_length=50, choices=TIPOS_PROBLEMA)
    descricao_problema = models.TextField()
    urgencia = models.CharField(max_length=50, choices=URGENCIAS, default='Estou sem pressa')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Pendente', 'Pendente'),
            ('Atendido', 'Atendido'),
        ],
        default='Pendente'
    )

    @property
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"

    def __str__(self):
        return f"{self.nome_completo} - {self.tipo_problema} ({self.status})"
