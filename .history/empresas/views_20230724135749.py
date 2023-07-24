from django.views.generic import TemplateView, DetailView  # Import do TemplateView para trabalhar com class based view
from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from core.models import Empregador
from empresas.models import Empresas, Sistemas, SistemaQtdFuncionarios
from usuarios.models import Permissao
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from datetime import date
import csv
from django.http import HttpResponseRedirect
from django.shortcuts import render
import chardet


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
        next(csv_data)  # Ignorar cabeçalho do CSV

        empresas = []
        for row in csv_data:
            empresa = Empresas(razao=row[0], cnpj=row[1], fantasia=row[2], nome_adicional=row[3], email=row[4], observacoes=row[5])
            empresas.append(empresa)

        Empresas.objects.bulk_create(empresas)  # Cadastrar vários elementos de uma vez

        return HttpResponseRedirect('/process/')

    return render(request, 'upload_csv.html')




def is_csv_file(file):

        try:
            # Detectar o encoding do arquivo
            rawdata = file.read()
            result = chardet.detect(rawdata)
            encoding = result['encoding']

            # Decodificar o arquivo usando o encoding detectado
            decoded_file = rawdata.decode(encoding)

            # Processar o arquivo como CSV
            csv_data = list(csv.reader(decoded_file.splitlines(), delimiter=','))
            return True
        except (csv.Error, UnicodeDecodeError):
            return False

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
                autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                def vericarVazio(classe):
                    if not len(classe) == 0:
                        return classe[0]
                    else:
                        return
            
                empregador = Empregador.objects.all()
                empregador_item = vericarVazio(empregador)

                context = {
                    'empregador': empregador_item,
                    'empresas': empresas,
                    'sistemas': Sistemas.objects.all(),
                    'select': select,
                    'paginator': paginator,
                    'autorizacao': autorizacao
                }

                return render( request, 'listar-empresa.html', context)
            else:
                return redirect('/')


    def post(self, request):
        if request.method == 'POST' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            if csv_file.size > 20 * 1024 * 1024:
                messages.error(request, f'O arquivo ultrapassa o limite permitido de MB')
                return redirect('/listar-empresa')

            try:
                # Detectar o encoding do arquivo
                rawdata = csv_file.read()
                result = chardet.detect(rawdata)
                encoding = result['encoding']

                # Decodificar o arquivo usando o encoding detectado
                decoded_file = rawdata.decode(encoding)

                # Processar o arquivo como CSV
                csv_data = list(csv.reader(decoded_file.splitlines(), delimiter=','))

            except (csv.Error, UnicodeDecodeError):
                messages.error(request, 'Erro ao importar o arquivo CSV')
                return redirect('/listar-empresa')


            for row in csv_data[1:]:
                # Processar cada linha de dados aqui.
                print(f'{row[0]}-><-')


            count = 1
            for row in csv_data:
                empresa = Empresas(razao=row[0], cnpj=row[1], fantasia=row[2], nome_adicional=row[3], email=row[4], observacoes=row[5])
                count = count + 1
                error_message = Empresas.validarEmpresa(empresa)


                if error_message:
                    messages.error(request, f'Erro na linha {count}: {error_message}')
                    return redirect('/listar-empresa')

                if Sistemas.objects.filter(nome=row[6]).exists():
                    sistema = Sistemas.objects.get(nome=row[6])

                    error_message = Empresas.validarSistemaQtd(sistema.id, row[7], row[8], row[9])

                    if error_message:
                        messages.error(request, f'Erro na linha {count}: {error_message}')
                        return redirect('/listar-empresa')
                else:
                    messages.error(request, f'Erro na linha {count}: o nome do sistema não é válido')
                    return redirect('/listar-empresa')

            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
            #next(csv_data)

            for row in csv_data:
                print(row[6])
                empresa = Empresas(razao=row[0], cnpj=row[1], fantasia=row[2], nome_adicional=row[3], email=row[4], observacoes=row[5])
                Empresas.save(empresa)  # Cadastrar vários elementos de uma vez
                sistema = Sistemas.objects.get(nome=row[6])
                sistema_qtd_funcionarios = SistemaQtdFuncionarios(empresa = Empresas.objects.get(id=(empresa.id)),
                                                                    sistema = Sistemas.objects.get(id=int(sistema.id)),
                                                                    quantidade = row[7],
                                                                    contrato = row[8],
                                                                    suporte = row[9]
                                                                    )
                SistemaQtdFuncionarios.save(sistema_qtd_funcionarios)

            messages.success(request, 'Empresa(s) importada(s) com sucesso!')
            return redirect('/listar-empresa')




    template_name: str = 'listar-empresa.html'


class PesquisarEmView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_listar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).visualizar_empresa

            if aut_listar_empresa:

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

                autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                def vericarVazio(classe):
                    if not len(classe) == 0:
                        return classe[0]
                    else:
                        return
            
                empregador = Empregador.objects.all()
                empregador_item = vericarVazio(empregador)

                context = {
                    'empregador': empregador_item,
                        'empresas': empresas,
                        'sistemas': Sistemas.objects.all(),
                        'paginator': paginator,
                        'autorizacao': autorizacao
                    }

                return render( request, 'pesquisar-empresa.html', context)
            else:
                return redirect('/')
    

    template_name: str = 'pesquisar-empresa.html'


class CadastroEmView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_cadastrar_empresa = Permissao.objects.get(nome=request.session['usuario_permissao']).cadastrar_empresa
            if aut_cadastrar_empresa:

                autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                def vericarVazio(classe):
                    if not len(classe) == 0:
                        return classe[0]
                    else:
                        return
            
                empregador = Empregador.objects.all()
                empregador_item = vericarVazio(empregador)

                context = {
                    'empregador': empregador_item,
                    'sistemas': Sistemas.objects.all(),
                    'autorizacao': autorizacao
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

                if SistemaQtdFuncionarios.objects.filter(id=pk):
                    empresa = SistemaQtdFuncionarios.objects.get(id=pk)

                    autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

                    def vericarVazio(classe):
                        if not len(classe) == 0:
                            return classe[0]
                        else:
                            return

                    empregador = Empregador.objects.all()
                    empregador_item = vericarVazio(empregador)

                    context = {
                        'empregador': empregador_item,
                        'empresa' : empresa,
                        'sistemas': Sistemas.objects.all(),
                        'autorizacao': autorizacao
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

                messages.success(request, 'Empresa excluida com sucesso!')
                sistema_empresa = SistemaQtdFuncionarios.objects.get(id=pk)
                empresa = Empresas.objects.get(id=sistema_empresa.empresa.id)
                empresa.delete()
                sistema_empresa.delete()
            else:
                return redirect('/')

        return redirect('/listar-empresa')


    template_name: str = 'excluir-empresa.html'
