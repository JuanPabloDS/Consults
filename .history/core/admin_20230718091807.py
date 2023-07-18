from django.contrib import admin
from .models import Empregador

# Register your models here.

@admin.register(Empregador)
class EmpregadorAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia',)