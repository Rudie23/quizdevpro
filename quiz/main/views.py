from django.shortcuts import render


# Create your views here.
from quiz.main.models import Pergunta


def home(request):
    return render(request, 'base/home.html')


def classificacao(request):
    return render(request, 'base/classificacao.html')


def perguntas(request, indice):  # indice é o parametro passado na url
    pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]  # quero pegar a pergunta com o
    # mesmo indice que foi informador na url -/perguntas/indice. Como o indice em python começa em 0, eu coloco o -1
    ctx = {'indice_da_questao': indice,
           'pergunta': pergunta}  # o valor de indice será determinado pela url
    return render(request, 'base/game.html', context=ctx)
