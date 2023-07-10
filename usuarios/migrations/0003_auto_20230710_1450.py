# Generated by Django 3.2 on 2023-07-10 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20230710_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='permissao',
            old_name='empresa_cadastro',
            new_name='cadastrar_empresa',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='empresa_editar',
            new_name='cadastrar_treinamento',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='empresa_visualizar',
            new_name='cadastrar_usuario',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='treinamento_cadastro',
            new_name='editar_empresa',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='treinamento_editar',
            new_name='editar_treinamento',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='treinamento_visualizar',
            new_name='editar_usuario',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='usuario_cadastro',
            new_name='visualizar_empresa',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='usuario_editar',
            new_name='visualizar_treinamento',
        ),
        migrations.RenameField(
            model_name='permissao',
            old_name='usuario_visualizar',
            new_name='visualizar_usuario',
        ),
    ]