from django.views.generic import TemplateView  # Import do TemplateView para trabalhar com class based view
from django.views import View
from django.contrib.auth.hashers import check_password, make_password
from usuarios.models import Usuarios, Permissao
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import date
from django.core.paginator import Paginator, InvalidPage, EmptyPage


class UsuariosView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_visualizar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).visualizar_usuario
            if aut_visualizar_usuario:


                values = Usuarios.objects.all()
                usuarios = ''

                if not len(values) == 0:

                    paginator = Paginator(values, 15)

                    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
                    try:
                        page = int(request.GET.get('page', '1'))
                    except ValueError:
                        page = 1

                    # Se o page request (9999) está fora da lista, mostre a última página.
                    try:
                        usuarios = paginator.page(page)
                    except (EmptyPage, InvalidPage):
                        usuarios = paginator.page(paginator.num_pages)

                else:
                    paginator = ''


                autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                context = {
                    'autorizacao': autorizacao,
                    'paginator':paginator,
                    'usuarios': values,
                }



                return render(request, 'usuarios.html', context)
            else:
                return redirect('/')

    template_name: str = 'usuarios.html'

class EditarUsuariosView(TemplateView):


    def get(self, request, pk):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_usuario
            if aut_editar_usuario:
                aut_visualizar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).visualizar_usuario

                if not aut_visualizar_usuario:
                    autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                    context = {
                        'autorizacao': autorizacao,
                        'usuario':Usuarios.objects.get(id=int(request.session['usuario'])),

                    }


                    return render(request, 'editar-usuario.html', context)

                else:

                    autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                    context = {
                        'autorizacao': autorizacao,
                        'usuario':Usuarios.objects.get(id=pk),
                        'permissao':Permissao.objects.all()
                    }


                    return render(request, 'editar-usuario.html', context)
            else:
                
                return redirect('/')
    

    def post(self, request, pk):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_usuario
            if aut_editar_usuario:

                nome = request.POST.get('nome')
                user = request.POST.get('user')
                senha = request.POST.get('senha')
                conf_senha = request.POST.get('confirmar_senha')
                permissao = request.POST.get('permissao')
                edit_usuario = Usuarios.objects.get(id=pk)

                if senha == '':
                    senha = edit_usuario.senha
                elif conf_senha == '':
                    conf_senha = senha
                elif senha != conf_senha:
                    messages.error(request, 'As senhas não coincidem.')
                    return redirect(f'/editar-usuario/{pk}')

                if not edit_usuario.user == user:
                    if edit_usuario.isExists():
                        error_message = 'O usuário já existe.'


                """if not Permissao.objects.filter(id=int(permissao)).exists():

                    messages.error(request, 'A permissão para esse usuário não é válida')
                    return redirect(f'/editar-usuario/{pk}')"""

                # Criar o cliente
                usuario = Usuarios(
                                    id=pk,
                                    criado=edit_usuario.criado,
                                    modificado=date.today(),
                                    ativo=True,
                                    nome=nome,
                                    user=user,
                                    senha=senha,
                                    permissao_login=Permissao.objects.get(id=int(permissao)))

                error_message = Usuarios.validarUsuarioEdit(usuario)

                if not error_message:
                    """Se não tiver mensagem de erro"""
                    if senha == edit_usuario.senha:
                        usuario.register()
                        messages.success(request, 'Usuário alterado com sucesso!')
                        if int(request.session['usuario']) == pk:
                            request.session['usuario_nome'] = nome
                            messages.success(request, 'Usuário alterado com sucesso!')

                    else:
                        usuario.senha = make_password(usuario.senha)  # Cria a senha para usuario
                        usuario.register()  # Registrar o usuario no banco
                        messages.success(request, 'Usuário alterado com sucesso!')
                        if int(request.session['usuario']) == pk:
                            request.session['usuario_nome'] = nome

                    return redirect('/usuarios')
                else:
                    """Se existir dado invalidos retorna para página de erro"""
                    messages.error(request, error_message)
                    return redirect('/usuarios')
            else:
                return redirect('/')



    template_name: str = 'editar-usuario.html'

class NovoUsuarioView(TemplateView):


    def get(self, request):
        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:


            aut_cadastrar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).cadastrar_usuario
            if aut_cadastrar_usuario:

                autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                context = {
                    'autorizacao': autorizacao,
                    'permissao': Permissao.objects.all(),
                }

                return render(request, 'novo-usuario.html', context)
            else:
                return redirect('/')



    def post(self, request):
        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_cadastrar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).cadastrar_usuario
            if aut_cadastrar_usuario:


                nome = request.POST.get('nome')
                user = request.POST.get('user')
                senha = request.POST.get('senha')
                conf_senha = request.POST.get('confirmar_senha')
                permissao = request.POST.get('permissao')

                print(user)

                if senha == conf_senha:
                    pass
                else:
                    messages.error(request, 'As senhas digitadas não coincidem')
                    return redirect('/novo-usuario')

                if not Permissao.objects.filter(id=int(permissao)).exists():
                    messages.error(request, 'A permissão para esse usuário não é válida')
                    return redirect('/novo-usuario')

                # Criar o cliente
                usuario = Usuarios( nome=nome,
                                    user=user,
                                    senha=senha,
                                    permissao_login=Permissao.objects.get(id=int(permissao)))

                error_message = Usuarios.validarUsuario(usuario)

                if not error_message:
                    """Se não tiver mensagem de erro"""
                    usuario.senha = make_password(usuario.senha)  # Cria a senha para usuario
                    usuario.register()  # Registrar o usuario no banco
                    messages.success(request, 'Usuário cadastrado com sucesso!')
                    return redirect('/usuarios')
                else:
                    """Se existir dado invalidos retorna para página de erro"""
                    messages.error(request, error_message)
                    return redirect('/novo-usuario')
            else:
                return redirect('/')

class ExcluirUsuarioView(TemplateView):

    def get(self, request, pk):


        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_usuario = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_usuario
            if aut_editar_usuario:
                if request.session['usuario_permissao'] == str(Permissao.objects.get(id=3)):
                    return redirect('/listar-empresa')
                else:
                    messages.success(request, 'Usuário excluido com sucesso!')
                    usuario = Usuarios.objects.get(id=pk)
                    usuario.delete()
            else:
                return redirect('/')

        return redirect('/usuarios')


    template_name: str = 'excluir-usuario.html'