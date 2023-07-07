from django.db import models
from core.models import Base
from itertools import cycle



class Sistemas(models.Model):
    nome = models.CharField(max_length=50)

    def register(self):
        self.save()

    class Meta:
        verbose_name = 'Sistema'
        verbose_name_plural = 'Sistemas'

    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.nome}'




class Empresas(Base):
    razao = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    fantasia = models.CharField(max_length=100)
    nome_adicional = models.CharField(max_length=100)
    email = models.EmailField()
    observacoes = models.CharField(max_length=200)


    def register(self):
        self.save()

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.razao}'

    def is_cnpj_valido(cnpj: str) -> bool:

        # Limpando cnpj
        cnpj = cnpj.replace( "-", "" )
        cnpj = cnpj.replace( ".", "" )
        cnpj = cnpj.replace( "/", "" )

        LENGTH_CNPJ = 14

        if len(cnpj) != LENGTH_CNPJ:
            return False

        if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
            return False

        cnpj_r = cnpj[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1:i] != str(dv % 10):
                return False

        return True

    def isExistsEmail(self):
        """Verifica se o email existe no banco"""
        if Empresas.objects.filter(email=self.email):
            return True


    def isExistsCnpj(self):
        """Busca o email cadastrado dentro do banco"""
        if Empresas.objects.filter(cnpj=self.cnpj).exists():
            return True


    def validarEmpresa(empresa):
        """Função criada para validação dos dados do usuario"""
        error_message = None

        if (not empresa.razao):
            error_message = 'Insira o nome corretamente'
        elif len(empresa.razao) < 3:
            error_message = 'A empresa precisa ter mais do que 3 letras'
        elif len(empresa.razao) > 100:
            error_message = 'A empresa não pode ter mais do que 100 letras'
        elif len(empresa.cnpj) != 18:
            error_message = 'Cnpj dever conter apenas 14 números'
        elif len(empresa.fantasia) < 3:
            error_message = 'O nome fantasia precisa ter mais do que 3 letras'
        elif len(empresa.fantasia) > 100:
            error_message = 'o empresa não pode ter mais do que 100 letras'
        elif len(empresa.email) < 5:
            error_message = 'Email deve ter mais do 5 caracteres'
        elif len(empresa.email) > 50:
            error_message = 'Email deve ter menos do que 50 caracteres'
        elif len(empresa.observacoes) > 200:
            error_message = 'Observações deve ter no máximo 200 caracteres'
        elif Empresas.is_cnpj_valido(empresa.cnpj) == False:
            error_message = 'Cnpj é inválido.'


        return error_message


    def validarSistemaQtd(sistema, quantidade, contrato, suporte ):
        """Função criada para validação dos dados do usuario"""
        error_message = None

        if not Sistemas.objects.filter(id=int(sistema)).exists():
            error_message = 'O Sistema para essa empresa é inválido.'
        if (int(quantidade)) < 0:
            error_message = 'Quantidade de funcionarios é insuficiente'
        elif (int(quantidade)) > 1000:
            error_message = 'A quantidade de funcionários excede o limite'
        elif contrato != 'Mensal':
            if contrato != 'Anual':
                error_message = 'O contrato não é válido'
        elif len(contrato) > 10:
            error_message = 'O contrato não é válido'
        elif suporte != 'Sim':
            if suporte != 'Não':
                error_message = 'Suporte técnico inválido. '
        elif len(suporte) > 10:
            error_message = 'Suporte técnico inválido.'

        return error_message





class SistemaQtdFuncionarios(Base):
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    sistema =  models.ForeignKey(Sistemas, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    contrato = models.CharField(max_length=10)
    suporte = models.CharField(max_length=3)

    def register(self):
        self.save()

    class Meta:
        verbose_name = 'Sistema e quantidade de funcionario'
        verbose_name_plural = 'Sistemas e quantidades de funcionarios'

    def __str__(self) -> str:
        """Retorna o str"""
        return f'{self.sistema} - {self.quantidade} Funcionarios'




