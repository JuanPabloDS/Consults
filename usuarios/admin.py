from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Usuarios, Permissao

@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)


class UsuariosAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Verifica se a senha foi modificada
        if 'senha' in form.changed_data:
            obj.senha = make_password(obj.senha)
        
        super().save_model(request, obj, form, change)

admin.site.register(Usuarios, UsuariosAdmin)

