# Generated by Django 4.1 on 2023-02-07 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
        ('core', '0001_initial'),
        ('empresas', '0005_alter_sistemaqtdfuncionarios_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreinamentoStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Treinamento Status',
                'verbose_name_plural': 'Treinamentos status',
            },
        ),
        migrations.CreateModel(
            name='Treinamentos',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.base')),
                ('empresa', models.CharField(max_length=101)),
                ('cnpj', models.CharField(max_length=20)),
                ('cliente', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=100)),
                ('data', models.CharField(max_length=100)),
                ('horario', models.CharField(max_length=100)),
                ('observacao', models.CharField(max_length=300)),
                ('atendente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
                ('sistem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas.sistemas')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treinamentos.treinamentostatus')),
            ],
            options={
                'verbose_name': 'Treinamento',
                'verbose_name_plural': 'Treinamentos',
            },
            bases=('core.base',),
        ),
    ]
