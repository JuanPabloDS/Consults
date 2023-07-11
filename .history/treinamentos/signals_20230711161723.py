from django.db.models.signals import post_migrate
from django.dispatch import receiver
from treinamentos.models import TreinamentoStatus

@receiver(post_migrate)
def criar_objeto_inicial(sender, **kwargs):
    print('fdfdfdfdfdf')
    if TreinamentoStatus.objects.exists():
        # Já existe um objeto, não é necessário criar novamente
        return

    # Criação do objeto inicial
    meu_objeto = TreinamentoStatus('Aberto')
    meu_objeto_2 = TreinamentoStatus('Aberto')
    meu_objeto.save()
    meu_objeto_2.save()
