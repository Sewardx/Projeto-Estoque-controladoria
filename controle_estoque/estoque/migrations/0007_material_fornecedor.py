# Generated by Django 5.1.3 on 2024-11-28 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estoque", "0006_alter_material_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="material",
            name="fornecedor",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
