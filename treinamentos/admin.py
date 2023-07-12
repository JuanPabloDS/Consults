from django.contrib import admin

from .models import Treinamentos



@admin.register(Treinamentos)
class TreinamentosAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cliente', 'telefone', 'sistema', 'data', 'horario', 'observacao', 'status', 'criado', 'modificado', 'ativo',)
