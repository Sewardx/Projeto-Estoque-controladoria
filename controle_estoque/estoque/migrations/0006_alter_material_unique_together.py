# Generated by Django 5.1.3 on 2024-11-26 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("estoque", "0005_alter_material_tipo_produto"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="material",
            unique_together={("nome", "tipo_produto")},
        ),
    ]
