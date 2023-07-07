from django.contrib import admin

from .models import Sistemas, SistemaQtdFuncionarios, Empresas


@admin.register(Sistemas)
class SistemasAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('id', 'razao', 'cnpj', 'fantasia', 'nome_adicional', 'email', 'observacoes', 'criado', 'modificado', 'ativo',)


@admin.register(SistemaQtdFuncionarios)
class SistemaQtdFuncionariosAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'sistema', 'quantidade', 'contrato', 'suporte','criado', 'modificado', 'ativo',)

