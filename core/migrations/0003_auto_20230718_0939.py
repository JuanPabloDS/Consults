# Generated by Django 3.2 on 2023-07-18 12:39

import core.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_empregador'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empregador',
            options={'verbose_name': 'Empregador', 'verbose_name_plural': 'Empregador'},
        ),
        migrations.AlterField(
            model_name='empregador',
            name='icone_do_site_icon',
            field=stdimage.models.StdImageField(force_min_size=False, help_text='Icone que aparece no navegador ao visitar o site. Formato precisa ser ".icon"', upload_to=core.models.get_file_path, variations={}, verbose_name='icone da empresa'),
        ),
        migrations.AlterField(
            model_name='empregador',
            name='imagem_empresa',
            field=stdimage.models.StdImageField(force_min_size=False, help_text='Imagem usada como icone da empresa', upload_to=core.models.get_file_path, variations={}, verbose_name='Imagem da empresa'),
        ),
    ]