# Generated by Django 3.2 on 2023-07-12 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treinamentos', '0002_auto_20230712_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treinamentos',
            name='observacao',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
