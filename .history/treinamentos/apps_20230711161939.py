from django.apps import AppConfig
from treinamentos.models import TreinamentoStatus


class TreinamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treinamentos'

    if TreinamentoStatus.objects.exists():
        # Já existe um objeto, não é necessário criar novamente
        pass
    else:

        # Criação do objeto inicial
        meu_objeto = TreinamentoStatus('Aberto')
        meu_objeto_2 = TreinamentoStatus('Fechado')
        meu_objeto.save()
        meu_objeto_2.save()