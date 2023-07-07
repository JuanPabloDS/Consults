# Generated by Django 4.1 on 2023-01-24 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresas',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.base')),
                ('razao', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=20)),
                ('fantasia', models.CharField(max_length=100)),
                ('nome_adicional', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('observacoes', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
            bases=('core.base',),
        ),
        migrations.CreateModel(
            name='SistemaQtdFuncionarios',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.base')),
                ('quantidade', models.IntegerField()),
                ('contrato', models.CharField(max_length=10)),
                ('razao', models.CharField(max_length=100)),
                ('suporte', models.CharField(max_length=3)),
            ],
            bases=('core.base',),
        ),
        migrations.CreateModel(
            name='Sistemas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SistemasEmpresa',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.base')),
                ('Sistema_qtd_funcionarios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas.sistemaqtdfuncionarios')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas.empresas')),
            ],
            options={
                'verbose_name': 'Sistema da empresa',
                'verbose_name_plural': 'Sistemas das empresa',
            },
            bases=('core.base',),
        ),
        migrations.AddField(
            model_name='sistemaqtdfuncionarios',
            name='sistema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas.sistemas'),
        ),
    ]