# Generated by Django 5.1.3 on 2024-11-26 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estoque", "0004_rename_codigo_produto_material_tipo_produto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="material",
            name="tipo_produto",
            field=models.CharField(default="DEFAULT_CODE", max_length=50),
        ),
    ]
