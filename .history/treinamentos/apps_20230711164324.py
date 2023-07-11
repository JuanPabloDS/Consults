from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TreinamentoStatus

@receiver(post_migrate)
def criar_objeto_inicial(sender, **kwargs):
    if TreinamentoStatus.objects.exists():
        # Já existe um objeto, não é necessário criar novamente
        return

    # Criação do objeto inicial
    meu_objeto = TreinamentoStatus('Aberto')
    meu_objeto_2 = TreinamentoStatus('Fechado')
    meu_objeto.save()
    meu_objeto_2.save()


class TreinamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treinamentos'

    
    def ready(self):
        criar_objeto_inicial()