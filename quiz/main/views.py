from django.db.models import Sum
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.timezone import now

from quiz.main.forms import AlunoForm
from quiz.main.models import Pergunta, Aluno, Resposta


def home(request):
    if request.method == 'POST':
        # Usuario ja existe
        email = request.POST['email']
        try:
            aluno = Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            # Usuario nao existe
            formulario = AlunoForm(request.POST)
            if formulario.is_valid():
                aluno = formulario.save()
                request.session['aluno_id'] = aluno.id
                return redirect('/perguntas/1')
            else:  # se os dados enviados pelo post não estiverem corretos, esses ainda serão salvos
                ctx = {'formulario': formulario}
                return render(request, 'base/home.html', ctx)
        else:  # se não der erro
            request.session['aluno_id'] = aluno.id  # cria uma sessão com o nome aluno_id
            return redirect('/perguntas/1')

    return render(request, 'base/home.html')


def classificacao(request):
    try:
        aluno_id = request.session['aluno_id']
    except KeyError:
        return redirect('/')
    else:
        pontos_dct = Resposta.objects.filter(aluno_id=aluno_id).aggregate(Sum('pontos'))
        pontuacao_do_aluno = pontos_dct['pontos__sum']

        numero_de_alunos_com_maior_pontuacao = Resposta.objects.values('aluno').annotate(Sum('pontos')).filter(pontos__sum__gt = pontuacao_do_aluno).count()
        primeiros_alunos_da_classificacao = list(
            Resposta.objects.values('aluno', 'aluno__nome').annotate(Sum('pontos')).order_by('-pontos__sum')[:5])
        ctx = {'pontuacao_do_alun': pontuacao_do_aluno,
               'posicao_do_aluno': numero_de_alunos_com_maior_pontuacao + 1,
               'primeiros_alunos_da_classificacao': primeiros_alunos_da_classificacao
               }
        return render(request, 'base/classificacao.html', ctx)


PONTUACAO_MAXIMA = 1000


def perguntas(request, indice):  # indice é o parametro passado na url
    try:
        aluno_id = request.session['aluno_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]  # quero pegar a pergunta
            # com o mesmo indice que foi informador na url -/perguntas/indice. Como o indice em python começa em 0,
            # eu coloco o -1
        except IndexError:
            return redirect('/classificacao')
        else:
            ctx = {'indice_da_questao': indice,
                   'pergunta': pergunta}  # o valor de indice será determinado pela url
            if request.method == 'POST':
                resposta_indice = int(request.POST['resposta_indice'])
                if resposta_indice == pergunta.alternativa_correta:
                    # Armazenar dados da resposta
                    try:
                        data_da_pri_resposta = Resposta.objects.filter(pergunta=pergunta).order_by('respondida_em')[0].respondida_em
                        # Como eu quero apenas obter apenas a 1ª data resposta
                    except IndexError:
                        Resposta(aluno_id=aluno_id, pergunta=pergunta, pontos=PONTUACAO_MAXIMA).save()
                    else:
                        diferenca = now() - data_da_pri_resposta
                        diferenca_em_segundos = int(diferenca.total_seconds())
                        pontos = max(PONTUACAO_MAXIMA - diferenca_em_segundos, 10)
                        Resposta(aluno_id=aluno_id, pergunta=pergunta, pontos=pontos).save()
                    return redirect(f'/perguntas/{indice + 1}')
                ctx['resposta_indice'] = resposta_indice
            return render(request, 'base/game.html', context=ctx)
