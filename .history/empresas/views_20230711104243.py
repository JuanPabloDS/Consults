from django.views.generic import TemplateView, DetailView  # Import do TemplateView para trabalhar com class based view
from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from empresas.models import Empresas, Sistemas, SistemaQtdFuncionarios
from usuarios.models import Permissao
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from datetime import date



class ListarEmView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:


            aut_listar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).visualizar_empresa

            if aut_listar_empresa:

                values = SistemaQtdFuncionarios.objects.all().order_by('-id')
                select = ''
                empresas = ''

                if self.request.GET.get("search"):
                    """Recebe os dados da busca que são passados na URL"""

                    query = self.request.GET.get("search")


                    if query.isdigit():
                        values = SistemaQtdFuncionarios.objects.filter(
                            Q(sistema=query)
                        ).order_by('-id')

                        select = int(query)

                if not len(values) == 0:

                    paginator = Paginator(values, 15)

                    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
                    try:
                        page = int(request.GET.get('page', '1'))
                    except ValueError:
                        page = 1

                    # Se o page request (9999) está fora da lista, mostre a última página.
                    try:
                        empresas = paginator.page(page)
                    except (EmptyPage, InvalidPage):
                        empresas = paginator.page(paginator.num_pages)

                else:
                    paginator = ''

                context = {
                    'empresas': empresas,
                    'sistemas': Sistemas.objects.all(),
                    'select': select,
                    'paginator': paginator,
                }

                return render( request, 'listar-empresa.html', context)
            else:
                return redirect('/')



    template_name: str = 'listar-empresa.html'


class PesquisarEmView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:

            if self.request.GET.get("search"):
                    """Recebe os dados da busca que são passados na URL"""
                    query = self.request.GET.get("search")
            else:
                return redirect('/')

            values = SistemaQtdFuncionarios.objects.all().order_by('-id')



            if query:
                empresas = SistemaQtdFuncionarios.objects.filter(
                    Q(empresa__razao__icontains=query) | Q(empresa__cnpj__icontains=query) | Q(empresa__fantasia__icontains=query)
                    | Q(empresa__nome_adicional__icontains=query)

                    )



            if not len(empresas) == 0:

                paginator = Paginator(empresas, 15)

                # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
                try:
                    page = int(request.GET.get('page', '1'))
                except ValueError:
                    page = 1

                # Se o page request (9999) está fora da lista, mostre a última página.
                try:
                    empresas = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    empresas = paginator.page(paginator.num_pages)

            else:
                paginator = ''

            context = {
                    'empresas': empresas,
                    'sistemas': Sistemas.objects.all(),
                    'paginator': paginator,

                }



        return render( request, 'pesquisar-empresa.html', context)

    template_name: str = 'pesquisar-empresa.html'


class CadastroEmView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_cadastrar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).cadastrar_empresa
            if aut_cadastrar_empresa:

                context = {
                    'sistemas': Sistemas.objects.all(),
                }

                return render( request, 'cadastrar-empresa.html', context)
            else:
                return redirect('/')



    def post(self, request):
        """Faz o cadastro e verificação dos dados do cliente no banco via POST"""
        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_cadastrar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).cadastrar_empresa
            if aut_cadastrar_empresa:

                razao = request.POST.get('razao')
                cnpj = request.POST.get('cnpj')
                fantasia = request.POST.get('fantasia')
                nome_adicional = request.POST.get('nome_adicional')
                email = request.POST.get('email')
                observacoes = request.POST.get('observacao')


                """Cadastro do sistema e quantidade de pessoas"""
                sistema = request.POST.get('sistema')
                funcionarios = request.POST.get('funcionarios')
                contrato = request.POST.get('contrato')
                suporte = request.POST.get('suporte')



                    # Criar a emrpesa
                empresa = Empresas( razao=razao,
                                    cnpj=cnpj,
                                    fantasia=fantasia,
                                    nome_adicional=nome_adicional,
                                    email=email,
                                    observacoes=observacoes
                                    )




                error_message = Empresas.validarEmpresa(empresa)


                if not error_message:
                    """Se não tiver mensagem de erro"""
                    error_message = Empresas.validarSistemaQtd(sistema, funcionarios, contrato, suporte)

                    if not error_message:
                        empresa.register()  # Registrar empresa

                        sistema_qtd_funcionarios = SistemaQtdFuncionarios(  empresa = Empresas.objects.get(id=(empresa.id)),
                                                                        sistema = Sistemas.objects.get(id=int(sistema)),
                                                                        quantidade = funcionarios,
                                                                        contrato = contrato,
                                                                        suporte = suporte
                                                                        )

                        messages.success(request, 'Empresa cadastrada com sucesso!')
                        sistema_qtd_funcionarios.register()

                        return redirect('/listar-empresa')
                    else:
                        """Se existir dado invalidos retorna para página de erro"""
                        messages.error(request, error_message)
                        return redirect('/cadastrar-empresa')
                else:
                    """Se existir dado invalidos retorna para página de erro"""
                    messages.error(request, error_message)
                    return redirect('/cadastrar-empresa')
            else:
                return redirect('/')



    template_name: str = 'cadastrar-empresa.html'

class EditarEmView(DetailView):

    queryset = SistemaQtdFuncionarios.objects.all()
    template_name: str = 'editar-empresa.html'


    def get(self, request, pk):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_empresa

            if aut_editar_empresa:
                if request.session['usuario_permissao'] == str(Permissao.objects.get(id=3)):
                    return redirect('/listar-empresa')
                else:
                    if SistemaQtdFuncionarios.objects.filter(id=pk):
                        empresa = SistemaQtdFuncionarios.objects.get(id=pk)

                        context = {
                            'empresa' : empresa,
                            'sistemas': Sistemas.objects.all()
                        }


                        return render( request, 'editar-empresa.html', context)

                    else:
                        messages.error(request, 'Empresa não encontrada')
                        return redirect('/listar-empresa')
            else:
                return redirect('/')


    def post(self, request, pk):
        """Faz o cadastro e verificação dos dados do cliente no banco via POST"""

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_empresa

            if aut_editar_empresa:

                empre_edi = SistemaQtdFuncionarios.objects.get(id=pk)


                razao = request.POST.get('razao')
                cnpj = request.POST.get('cnpj')
                fantasia = request.POST.get('fantasia')
                nome_adicional = request.POST.get('nome_adicional')
                email = request.POST.get('email')
                observacoes = request.POST.get('observacao')


                """Cadastro do sistema e quantidade de pessoas"""
                sistema = request.POST.get('sistema')
                funcionarios = request.POST.get('funcionarios')
                contrato = request.POST.get('contrato')
                suporte = request.POST.get('suporte')


                empresa = Empresas.objects.get(pk=empre_edi.empresa.id)

                    # Criar a emrpesa
                empr = Empresas(    id=empre_edi.empresa.id,
                                    criado=empresa.criado,
                                    modificado=date.today(),
                                    ativo=True,
                                    razao=razao,
                                    cnpj=cnpj,
                                    fantasia=fantasia,
                                    nome_adicional=nome_adicional,
                                    email=email,
                                    observacoes=observacoes
                                    )

                error_message = Empresas.validarEmpresa(empr)


                if not error_message:
                    """Se não tiver mensagem de erro"""
                    error_message = Empresas.validarSistemaQtd(sistema, funcionarios, contrato, suporte)

                    if not error_message:
                        empr.register()  # Registrar empresa
                        sistema_qtd_func = SistemaQtdFuncionarios.objects.get(pk=pk)
                        sistema_qtd_funcionarios = SistemaQtdFuncionarios(  id=pk,
                                                                            criado=sistema_qtd_func.criado,
                                                                            modificado=date.today(),
                                                                            ativo=True,
                                                                            empresa = Empresas.objects.get(id=(empr.id)),
                                                                            sistema = Sistemas.objects.get(id=int(sistema)),
                                                                            quantidade = funcionarios,
                                                                            contrato = contrato,
                                                                            suporte = suporte
                                                                        )

                        sistema_qtd_funcionarios.register()

                        return redirect('/listar-empresa')
                    else:
                        """Se existir dado invalidos retorna para página de erro"""
                        messages.error(request, error_message)
                        return redirect(f'/editar-empresa/{pk}')
                else:
                    """Se existir dado invalidos retorna para página de erro"""
                    messages.error(request, error_message)
                    return redirect(f'/editar-empresa/{pk}')
            else:
                return redirect('/')


class ExcluirEmView(TemplateView):

    def get(self, request, pk):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_empresa

            if aut_editar_empresa:

                if request.session['usuario_permissao'] == str(Permissao.objects.get(id=3)):
                    return redirect('/listar-empresa')
                else:
                    messages.success(request, 'Empresa excluida com sucesso!')
                    sistema_empresa = SistemaQtdFuncionarios.objects.get(id=pk)
                    empresa = Empresas.objects.get(id=sistema_empresa.empresa.id)
                    empresa.delete()
                    sistema_empresa.delete()
            else:
                return redirect('/')

        return redirect('/listar-empresa')


    template_name: str = 'excluir-empresa.html'
