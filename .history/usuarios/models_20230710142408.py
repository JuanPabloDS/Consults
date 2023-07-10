from django.db import models
from core.models import Base



class Permissao(Base):
    nome = models.CharField('Nome da permissão?',max_length=50)
    empresa_cadastro = models.BooleanField('Permissão para cadastrar empresa?', default=False)
    empresa_editar = models.BooleanField('Permissão para editar empresa?', default=False)
    empresa_visualizar = models.BooleanField('Permissão para visualizar empresa?', default=False)
    treinamento_cadastro = models.BooleanField('Permissão para cadstrar treinamento?', default=False)
    treinamento_editar = models.BooleanField('Permissão para editar treinamento?', default=False)
    treinamento_visualizar = models.BooleanField('Permissão para visualizar treinamento?', default=False)
    usuario_cadastro = models.BooleanField('Permissão para cadstrar usuário?', default=False)
    usuario_editar = models.BooleanField('Permissão para editar usuário?', default=False)
    usuario_visualizar = models.BooleanField('Permissão para visualizar usuário?', default=False)


    # Salvar os dados no banco
    def register(self):
        self.save()
    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'

    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.nome}'


class Usuarios(Base):
    nome = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    senha = models.CharField(max_length=100)
    permissao_login = models.ForeignKey(Permissao, on_delete=models.CASCADE)

    # Salvar os dados no banco
    def register(self):
        self.save()

    class Meta:
        verbose_name = 'Usuario do sistema'
        verbose_name_plural = 'Usuarios do sistema'

    @staticmethod
    def get_cliente_by_usuario(user):
        """Busca o email cadastrado dentro do banco"""
        try:
            return Usuarios.objects.get(user=user)
        except:
            return False

    def isExists(self):
        """Verifica se o email existe no banco"""
        if Usuarios.objects.filter(user=self.user):
            return True

        return False

    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.nome}'

    def validarUsuario(usuario):
        """Função criada para validação dos dados do usuario"""
        error_message = None

        if (not usuario.nome):
            error_message = 'Insira o nome corretamente'
        elif len(usuario.nome) < 3:
            error_message = 'Nome precisa ter mais do que 3 caracteres'
        elif len(usuario.nome) > 50:
            error_message = 'Nome precisa ter menos do que 50 caracteres'
        elif len(usuario.senha) < 5:
            error_message = 'Senha dever ter mais do que 5 caracteres'
        elif len(usuario.senha) > 100:
            error_message = 'Senha dever ter menos do que 100 caracteres'
        elif len(usuario.user) < 5:
            error_message = 'O usuário deve ter mais do 5 caracteres'
        elif len(usuario.user) > 50:
            error_message = 'O usuário deve ter menos do que 50 caracteres'
        elif usuario.isExists():
            error_message = 'O usuário já existe.'

        return error_message
    
    def validarUsuarioEdit(usuario):
        """Função criada para validação dos dados do usuario"""
        error_message = None

        if (not usuario.nome):
            error_message = 'Insira o nome corretamente'
        elif len(usuario.nome) < 3:
            error_message = 'Nome precisa ter mais do que 3 caracteres'
        elif len(usuario.nome) > 50:
            error_message = 'Nome precisa ter menos do que 50 caracteres'
        elif len(usuario.senha) < 5:
            error_message = 'Senha dever ter mais do que 5 caracteres'
        elif len(usuario.senha) > 100:
            error_message = 'Senha dever ter menos do que 100 caracteres'
        elif len(usuario.user) < 5:
            error_message = 'O usuário deve ter mais do 5 caracteres'
        elif len(usuario.user) > 50:
            error_message = 'O usuário deve ter menos do que 100 caracteres'

        return error_message


