from django.urls import path


from .views import (
    CadastroEmView, ListarEmView, EditarEmView, ExcluirEmView, PesquisarEmView
    )

urlpatterns = [
    path('cadastrar-empresa', CadastroEmView.as_view(), name='cadastrar-empresa'),
    path('listar-empresa', ListarEmView.as_view(), name='listar-empresa'),
    path('pesquisar-empresa/', PesquisarEmView.as_view(), name='pesquisar-empresa'),
    path('editar-empresa/<int:pk>', EditarEmView.as_view(), name='editar-empresa'),
    path('excluir-empresa/<int:pk>', ExcluirEmView.as_view(), name='excluir-empresa'),


]
