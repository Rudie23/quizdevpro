from django.contrib import admin

# Register your models here.
from quiz.main.models import Pergunta


@admin.register(Pergunta)
class AdminPergunta(admin.ModelAdmin):
    # Lembre-se: em alternativas use um dicionário JSON, EX - {"array":["function", "def", "if", "pass"]}
    list_display = ('id', 'enunciado', 'disponivel')
