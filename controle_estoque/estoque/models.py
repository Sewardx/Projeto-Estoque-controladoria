from django.db import models
from django.core.cache import cache
from django.core.exceptions import ValidationError

class Material(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=0)
    tipo_produto = models.CharField(max_length=50, default="DEFAULT_CODE")
    unidade = models.CharField(
        max_length=50,
        choices=[
            ('Unidade', 'Unidade'),
            ('Pacote', 'Pacote'),
            ('Caixa', 'Caixa'),
            ('Rolo', 'Rolo'),
            ('Cartucho', 'Cartucho'),
            ('Resma', 'Resma'),
            ('Frasco', 'Frasco'),
            ('Tubo', 'Tubo'),
            ('Par', 'Par'),
            ('Bloco', 'Bloco'),
            ('Kit', 'Kit'),
            ('Bobina', 'Bobina'),
            ('Galão', 'Galão'),
            ('Barra', 'Barra'),
            ('Livro', 'Livro'),
            ('Carrete', 'Carrete'),
            ('Lata', 'Lata'),
            ('Peça', 'Peça'),
            ('Metro', 'Metro'),
        ],
        default='Unidade'
    )
    fornecedor = models.CharField(max_length=100, blank=True, null=True)
    codigo_produto = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('nome', 'tipo_produto')
        verbose_name_plural = "Materiais"

    def __str__(self):
        return f"{self.nome} ({self.tipo_produto}) - {self.quantidade} {self.unidade}"

    def save(self, *args, **kwargs):
        # Ensures quantidade is never negative
        self.quantidade = max(0, self.quantidade)
        super().save(*args, **kwargs)
        cache.delete('materiais')

class RequisicaoDeMaterial(models.Model):
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField()
    departamento = models.CharField(max_length=100)
    data_requisicao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Aprovado', 'Aprovado'),
            ('Recusado', 'Recusado'),
        ],
        default='Pendente'
    )

    class Meta:
        verbose_name_plural = "Requisições de Material"
        ordering = ['-data_requisicao']

    def __str__(self):
        return f"{self.nome_completo} - {self.data_requisicao.strftime('%d/%m/%Y %H:%M')}"


class RequisicaoDeMaterialItem(models.Model):
    requisicao = models.ForeignKey(RequisicaoDeMaterial, on_delete=models.CASCADE, related_name="itens")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade_solicitada = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Itens de Requisição de Material"

    def __str__(self):
        return f"{self.material.nome} - {self.quantidade_solicitada} {self.material.unidade}"


class SolicitacaoCompra(models.Model):
    fornecedor = models.CharField(max_length=100)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pendente', 'Pendente'),
            ('Aprovado', 'Aprovado'),
            ('Recusado', 'Recusado'),
        ],
        default='Pendente'
    )

    class Meta:
        verbose_name_plural = "Solicitações de Compra"
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"{self.fornecedor} - {self.data_solicitacao.strftime('%d/%m/%Y %H:%M')}"

class SolicitacaoCompraItem(models.Model):
    solicitacao = models.ForeignKey(SolicitacaoCompra, on_delete=models.CASCADE, related_name="itens")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade_comprada = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Itens de Solicitação de Compra"

    def __str__(self):
        return f"{self.material.nome} - {self.quantidade_comprada} {self.material.unidade}"