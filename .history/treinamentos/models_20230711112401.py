from django.db import models
from core.models import Base
from empresas.models import Empresas
from usuarios.models import Usuarios
from datetime import date, datetime
from empresas.models import Sistemas





class TreinamentoStatus(models.Model):
    status = models.CharField(max_length=10)

    def register(self):
        self.save()

    class Meta:
        verbose_name = 'Treinamento Status'
        verbose_name_plural = 'Treinamentos status'

    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.status}'


class Treinamentos(Base):
    empresa = models.CharField(max_length=101)
    cnpj = models.CharField(max_length=20)
    cliente = models.CharField(max_length=50)
    telefone = models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    atendente = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    sistema = models.ForeignKey(Sistemas, on_delete=models.CASCADE)
    observacao = models.CharField(max_length=300)
    status = models.ForeignKey(TreinamentoStatus, on_delete=models.CASCADE)


    def register(self):
        self.save()

    class Meta:
        verbose_name = 'Treinamento'
        verbose_name_plural = 'Treinamentos'


    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.empresa}'


    def validarTreinamento(treinamento, sistema):
        """Função criada para validação dos dados do usuario"""
        error_message = None
        data_atual = date.today()
        print(treinamento.horario)

        try:
             data = datetime.strptime(treinamento.data, '%Y-%m-%d')
             data = data.date()
        except:
             error_message = 'A data é inválida.'
             return error_message


        if (not treinamento.empresa):
            error_message = 'Insira a nome da empresa corretamente'
        elif not Sistemas.objects.filter(id=int(sistema)).exists():
            error_message = 'O Sistema para essa treinamento é inválido.'
        elif len(treinamento.empresa) < 3:
            error_message = 'Nome da empresa precisa ter mais do que 3 caracteres'
        elif len(treinamento.empresa) > 100:
            error_message = 'Nome da empresa precisa ter menos do que 100 caracteres'
        elif len(treinamento.cnpj) != 18:
            error_message = 'Cnpj dever conter apenas 14 números'
        elif len(treinamento.cliente) < 3:
            error_message = 'O cliente precisa ter mais do que 3 caracteres'
        elif len(treinamento.cliente) > 100:
            error_message = 'O cliente precisa ter menos do que 100 caracteres'
        elif len(treinamento.observacao) > 200:
            error_message = 'Você atingiu o número maximo de caracteres em (observações) '
        elif Empresas.is_cnpj_valido(treinamento.cnpj) == False:
            error_message = 'Cnpj é inválido.'


        return error_message



