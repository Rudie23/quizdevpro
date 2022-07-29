from django.contrib import admin

# Register your models here.
from quiz.main.models import Pergunta, Aluno, Resposta


@admin.register(Pergunta)
class AdminPergunta(admin.ModelAdmin):
    # Lembre-se: em alternativas use um dicionário JSON, EX - {"array":["function", "def", "if", "pass"]}
    list_display = ('id', 'enunciado', 'disponivel')


@admin.register(Aluno)
class AdminAluno(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'criado_em')


@admin.register(Resposta)
class AdminResposta(admin.ModelAdmin):
    list_display = ('respondida_em', 'aluno', 'pergunta', 'pontos')
