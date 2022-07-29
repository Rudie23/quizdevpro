
from django.forms import ModelForm

from quiz.main.models import Aluno


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'email']
