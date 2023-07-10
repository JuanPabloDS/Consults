from django.views.generic import TemplateView  # Import do TemplateView para trabalhar com class based view
from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from usuarios.models import Usuarios, Permissao
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages



class LoginView(TemplateView):
    return_url = None

    def get(self, request):
        """Função get para visualização dos dados enviados pelo backend """


        if request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/')
        else:
            """Se não estiver logado é enviado para página de login"""
            return render(request, 'login.html')

    def post(self, request):
        """Faz a verificação dos dados do cliente ao enviar os dados via POST"""

        user = request.POST.get('user')
        senha = request.POST.get('senha')
        usuario = Usuarios.get_cliente_by_user(user)

        if usuario:
            """Verifica se o email inserido estava no banco de dados de usuarios"""

            flag = check_password(senha, usuario.senha) # Verifica se a senha inserida é a mesma do cliente

            if flag:
                request.session['usuario'] = usuario.id  # Salva o id do cliente na session
                nome = usuario.nome[0:16]  # Variavel contendo nome do usuario
                request.session['usuario_nome'] = nome
                request.session['usuario_permissao'] = str(usuario.permissao_login)  # Salvando nome na session
                # request.session['adm'] = str(Permissao.objects.get(id=1))
                r# equest.session['user'] = str(Permissao.objects.get(id=3))



                return redirect('/')

            else:
                messages.error(request, 'Login ou senha inválido(s)!' )
        else:
            messages.error(request, 'Login ou senha inválido(s)!' )

        return render(request, 'login.html')

    template_name: str = 'login.html'

def logout(request):
    request.session.pop('usuario')
    return redirect('/login')