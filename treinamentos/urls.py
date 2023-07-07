from django.urls import path

from .views import (
    TreinamentoAView, TreinamentoFView,
    AgendarTreinamentoView, EditarTreinamentoView, ExcluirTreinamentoView,
    FinalizarTreinamentoView
    )

urlpatterns = [
    path('treinamentos-abertos', TreinamentoAView.as_view(), name='treinamentos-abertos'),
    path('treinamentos-finalizados', TreinamentoFView.as_view(), name='treinamentos-finalizados'),
    path('agendar-treinamento', AgendarTreinamentoView.as_view(), name='agendar-treinamento'),
    path('editar-treinamento/<int:pk>', EditarTreinamentoView.as_view(), name='editar-treinamento'),
    path('excluir-treinamento/<int:pk>', ExcluirTreinamentoView.as_view(), name='excluir-treinamento'),
    path('finalizar-treinamento/<int:pk>', FinalizarTreinamentoView.as_view(), name='finalizar-treinamento'),



]
