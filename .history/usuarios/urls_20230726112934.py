from django.urls import path, include

from .views import (
    UsuariosView, NovoUsuarioView, EditarUsuariosView, ExcluirUsuarioView,
    )

urlpatterns = [
    path('usuarios', UsuariosView.as_view(), name='usuarios'),
    path('editar-usuario/<int:pk>', EditarUsuariosView.as_view(), name='editar-usuario'),
    path('excluir-usuario/<int:pk>', ExcluirUsuarioView.as_view(), name='excluir-usuario'),
    path('novo-usuario', NovoUsuarioView.as_view(), name='novo-usuario'),

]