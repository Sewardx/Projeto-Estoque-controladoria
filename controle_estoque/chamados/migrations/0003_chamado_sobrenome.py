# Generated by Django 5.1.3 on 2024-11-26 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chamados", "0002_chamado_numero_anydesk_chamado_ramal_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chamado",
            name="sobrenome",
            field=models.CharField(default="Sobrenome Padrão", max_length=100),
            preserve_default=False,
        ),
    ]
