# Generated by Django 5.1.3 on 2024-11-26 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("estoque", "0003_rename_solicitacao_requisicaodematerial_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="material",
            old_name="codigo_produto",
            new_name="tipo_produto",
        ),
    ]
