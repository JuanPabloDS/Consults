from django.apps import AppConfig


class TreinamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treinamentos'

    def ready(self):
        import treinamentos.signals  # Importando o arquivo signals.py