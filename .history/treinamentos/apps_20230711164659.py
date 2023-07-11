from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TreinamentoStatus

@receiver(post_migrate)
def criar_objeto_inicial(sender, **kwargs):
    if sender.name == 'treinamentos':
        if not TreinamentoStatus.objects.exists():

        # Criação do objeto inicial
            TreinamentoStatus.objects.create(status='Aberto')
            TreinamentoStatus.objects.create(status='Fechado')


class TreinamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treinamentos'


    def ready(self):
        post_migrate.connect(criar_objeto_inicial, sender=self)