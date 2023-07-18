from django.views.generic import TemplateView  # Import do TemplateView para trabalhar com class based view
from django.shortcuts import render, redirect
from usuarios.models import Permissao
from .models import Empregador
from empresas.models import Sistemas, Empresas, SistemaQtdFuncionarios
from treinamentos.models import Treinamentos
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q


class IndexView(TemplateView):

    def get(self, request):

        paginator = ''

        if not request.session.has_key('usuario'):
            """Se o cliente já estiver logado retorna para index"""
            return redirect('/login')
        else:
            request.session.set_expiry(32400)

            data = str(date.today())
            mes = data[5]+data[6]

            meses = {'01':'Jan','02': 'Fev','03': 'mar','04':  'abr', '05': 'maio', '06': 'jun','07': 'jul','08': 'ago','09': 'set','10': 'out','11': 'nov','12': 'dez'}

            for m in meses.keys():
                if mes == m:
                    data = f'{meses[m]} {data[8]}{data[9]}, {data[0]}{data[1]}{data[2]}{data[3]}'

            request.session['data'] = data

            values = Treinamentos.objects.filter(
                        Q(status='Aberto')
                    ).order_by('-id')

            trei_cont = len(values)

            treinamentos = values[:6]
            request.session['qtd_treinamentos'] = len(values)
            request.session['index'] = 'True'

            empresa = SistemaQtdFuncionarios.objects.all().order_by('-id')[:6]
            autorizacao = Permissao.objects.get(nome=request.session['usuario_permissao'])

            if not len(empresa) == 0:
                paginator = 1

            def vericarVazio(classe):
                if not len(classe) == 0:
                    return classe[0]
                else:
                    return
            
            empregador = Empregador.objects.all()
            empregador_item = vericarVazio(empregador)

            context = {
                'treinamentos': treinamentos,
                'empresas': empresa,
                'trein_cont': trei_cont,
                'paginator': paginator,
                'autorizacao': autorizacao,
                'empregador': empregador_item,
            }


            return render(request, 'index.html', context)

    template_name: str = 'index.html'

