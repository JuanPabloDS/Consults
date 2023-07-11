from django.views.generic import TemplateView  # Import do TemplateView para trabalhar com class based view
from django.views import View
from django.shortcuts import render, redirect, HttpResponseRedirect
from treinamentos.models import Treinamentos, TreinamentoStatus
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from empresas.models import Sistemas
from usuarios.models import Usuarios, Permissao
from datetime import date
from django.db.models import Q
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.views.generic import TemplateView  # Import do TemplateView para trabalhar com class based view


class TreinamentoAView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_visualizar_treinamento = Permissao.objects.get(nome=request.session['usuario_permissao']).visualizar_treinamento
            if aut_visualizar_treinamento:

                treinamentos = ''

                request.session['situacao'] = 'abertos'


                values = Treinamentos.objects.filter(
                            Q(status=1)
                        ).order_by('-id')


                if not len(values) == 0:

                    paginator = Paginator(values, 15)

                    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
                    try:
                        page = int(request.GET.get('page', '1'))
                    except ValueError:
                        page = 1

                    # Se o page request (9999) está fora da lista, mostre a última página.
                    try:
                        treinamentos = paginator.page(page)
                    except (EmptyPage, InvalidPage):
                        treinamentos = paginator.page(paginator.num_pages)

                else:
                    paginator = ''


                context = {
                    'treinamentos': treinamentos,
                    'paginator': paginator,
                }


                return render( request, 'treinamentos-abertos.html', context)
            else:
                return redirect('/')



    template_name: str = 'treinamentos-abertos.html'

class TreinamentoFView(TemplateView):

    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_visualizar_treinamento = Permissao.objects.get(nome=request.session['usuario_permissao']).visualizar_treinamento
            if aut_visualizar_treinamento:

                request.session['situacao'] = 'finalizados'
                treinamentos = ''


                values = Treinamentos.objects.filter(
                            Q(status=2)
                        ).order_by('-id')

                if not len(values) == 0:

                    paginator = Paginator(values, 15)

                    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
                    try:
                        page = int(request.GET.get('page', '1'))
                    except ValueError:
                        page = 1

                    # Se o page request (9999) está fora da lista, mostre a última página.
                    try:
                        treinamentos = paginator.page(page)
                    except (EmptyPage, InvalidPage):
                        treinamentos = paginator.page(paginator.num_pages)

                else:
                    paginator = ''


                context = {
                        'treinamentos':treinamentos,
                        'paginator': paginator,
                }


                return render( request, 'treinamentos-finalizados.html', context)
            else:
                return redirect('/')

    template_name: str = 'treinamentos-finalizados.html'

class AgendarTreinamentoView(TemplateView):



    def get(self, request):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_cadastrar_treinamento = Permissao.objects.get(nome=request.session['usuario_permissao']).cadastrar_treinamento
            if aut_cadastrar_treinamento:
                data_atual = str(date.today())

                context = {
                    'usuarios': Usuarios.objects.all(),
                    'data': data_atual,
                    'sistemas': Sistemas.objects.all(),
                }

                return render( request, 'agendar-treinamento.html', context)
            else:
                return redirect('/')



    def post(self, request):
        """Faz a verificação dos dados do cliente ao enviar os dados via POST"""

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:

            """Cadastro do treinamento """
            empresa = request.POST.get('empresa')
            cnpj = request.POST.get('cnpj')
            cliente = request.POST.get('cliente')
            telefone = request.POST.get('telefone')
            data = request.POST.get('data')
            horario = request.POST.get('horario')
            atendente = request.POST.get('atendente')
            observacao = request.POST.get('observacao')
            sistema = request.POST.get('sistema')

            print(atendente)

            if not request.session['adm'] == request.session['usuario_permissao']:
                atendente = Usuarios.objects.get(id=int(request.session['usuario']))
            else:

                if not Usuarios.objects.filter(id=atendente):

                        messages.error(request, 'Usuário para esse atendimento é inválido!')
                        return redirect('/novo-usuario')
                else:
                    atendente = Usuarios.objects.get(id=atendente)

            treinamento = Treinamentos(
                    empresa = empresa,
                    cnpj = cnpj,
                    cliente = cliente,
                    telefone = telefone,
                    data = data,
                    horario = horario,
                    atendente = atendente,
                    sistema = Sistemas.objects.get(id=int(sistema)),
                    observacao = observacao,
                    status = TreinamentoStatus.objects.get(id=1)
                )


            error_message = Treinamentos.validarTreinamento(treinamento, sistema)


            if not error_message:
                messages.success(request, 'Treinamento agendado com sucesso!')
                treinamento.register()  # Registrar

                return redirect('/treinamentos-abertos')
            else:
                    """Se existir dado invalidos retorna para página de erro"""
                    messages.error(request, error_message)
                    return redirect('/agendar-treinamento')




    template_name: str = 'agendar-treinamento.html'


class ExcluirTreinamentoView(TemplateView):

     def get(self, request, pk) :

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_treinamento = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_treinamento
            if aut_editar_treinamento:

                treinamento = Treinamentos.objects.get(id=pk)
                treinamento.delete()


                situacao = request.session['situacao']
                return redirect(f'/treinamentos-{situacao}')
            else:
                return redirect('/')



class EditarTreinamentoView(TemplateView):


    def get(self, request, pk):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            aut_editar_treinamento = Permissao.objects.get(nome=request.session['usuario_permissao']).editar_treinamento
            if aut_editar_treinamento:

                if Treinamentos.objects.filter(id=pk):

                    treinamento_edt = Treinamentos.objects.get(id=pk)

                    context = {
                        'treinamento':treinamento_edt,
                        'usuarios':Usuarios.objects.all(),
                        'sistemas': Sistemas.objects.all(),
                        'status': TreinamentoStatus.objects.all(),

                    }


                    return render( request, 'editar-treinamento.html', context)

                else:
                    messages.error(request, 'Treinamento não encontrada')
                    situacao = request.session['situacao']
                    return redirect(f'/treinamentos-{situacao}')
            else:
                return redirect('/')

    def post(self, request, pk):
        """Faz a verificação dos dados do cliente ao enviar os dados via POST"""

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:

            """Cadastro do treinamento """
            empresa = request.POST.get('empresa')
            cnpj = request.POST.get('cnpj')
            cliente = request.POST.get('cliente')
            telefone = request.POST.get('telefone')
            data = request.POST.get('data')
            horario = request.POST.get('horario')
            atendente = request.POST.get('atendente')
            observacao = request.POST.get('observacao')
            sistema = request.POST.get('sistema')
            status = request.POST.get('status')

            if not Usuarios.objects.filter(id=atendente):

                    messages.error(request, 'Usuário para esse atendimento é inválido!')
                    return redirect('/novo-usuario')
            else:
                atendente = Usuarios.objects.get(id=atendente)

            
            treinamento_edit = Treinamentos.objects.get(id=pk)

            treinamento = Treinamentos(
                    id=pk,
                    criado=treinamento_edit.criado,
                    modificado=date.today(),
                    ativo=True,
                    empresa = empresa,
                    cnpj = cnpj,
                    cliente = cliente,
                    telefone = telefone,
                    data = data,
                    horario = horario,
                    atendente = atendente,
                    sistema = Sistemas.objects.get(id=int(sistema)),
                    observacao = observacao,
                    status = TreinamentoStatus.objects.get(id=status)
                )


            error_message = Treinamentos.validarTreinamento(treinamento, sistema)


            if not error_message:
                treinamento.register()  # Registrar
                situacao = request.session['situacao']
                return redirect(f'/treinamentos-{situacao}')
            else:
                    """Se existir dado invalidos retorna para página de erro"""
                    messages.error(request, error_message)
                    situacao = request.session['situacao']
                    return redirect(f'/editar-treinamento/{pk}')



    template_name: str = 'editar-treinamento.html'



class FinalizarTreinamentoView(TemplateView):

    def get(self, request, pk):

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            if request.session['usuario_permissao'] == str(Permissao.objects.get(id=3)):
                return redirect('/treinamentos-abertos')
            else:

                treinamento = Treinamentos.objects.get(id=pk)
                treinamento.status = TreinamentoStatus.objects.get(id=2)
                treinamento.save()


                return redirect(f'/')



    template_name: str = 'finalizar-treinamento.html'
