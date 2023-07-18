from django.db import models
import uuid
from stdimage.models import StdImageField
from django.core.validators import RegexValidator

class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('data de Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

def get_file_path(_instance, filename):
    """ Função para gerar nomes aleátorios quando for salvar um
    arquivo de imagem"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class Empregador(Base):
    nome_fantasia = models.CharField(max_length=150)
    imagem_empresa = StdImageField('icon',upload_to=get_file_path, help_text='Imagem usada como icone da empresa')
    icone_do_site_icon = StdImageField('icon',upload_to=get_file_path, help_text='Icone que aparece no navegador ao visitar o site. Formato precisa ser ".icon"')

    class Meta:
        verbose_name = 'Empregador'
        verbose_name_plural = 'Empregador'


    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.nome_fantasia}'
