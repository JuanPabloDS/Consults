# Generated by Django 4.1 on 2023-01-24 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0003_alter_sistemaqtdfuncionarios_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemaqtdfuncionarios',
            name='empresa',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='empresas.empresas'),
        ),
        migrations.DeleteModel(
            name='SistemasEmpresa',
        ),
    ]
