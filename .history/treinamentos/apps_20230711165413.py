from django.apps import AppConfig
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django import setup


class TreinamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treinamentos'

    from .models import TreinamentoStatus



"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django import setup
from .models import TreinamentoStatus



class TreinamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treinamentos'

    def ready(self):
        @receiver(post_migrate)
        def criar_objeto_inicial(sender, **kwargs):
            if sender.name == 'treinamentos':
                if not TreinamentoStatus.objects.exists():

                # Criação do objeto inicial
                    TreinamentoStatus.objects.create(status='Aberto')
                    TreinamentoStatus.objects.create(status='Fechado')
        setup()
"""
