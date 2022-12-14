from django.db import models


# Create your models here.

# mvt (model view template)

class Aluno(models.Model):
    nome = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Pergunta(models.Model):
    enunciado = models.TextField()
    alternativas = models.JSONField()  # modelo permite ter uma hierarquia em JSON que permite colocar várias opções
    disponivel = models.BooleanField(default=False)
    alternativa_correta = models.IntegerField(choices=[  # um numero inteiro que vai indicar o indice da alternatica
        # correta
        (0, 'A'),  # o primeiro elemto (0) será armazenado no BD e o segundo valor aparecerá na tela
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
    ])

    def __str__(self):
        return self.enunciado


class Resposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)  # se eu apago um Aluno, eu apago a resposta
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    pontos = models.IntegerField()
    respondida_em = models.DateTimeField(auto_now_add=True)

    # Quero colocar que o usuario possa responder, de forma correta, APENAS UMA VEZ A PERGUNTA
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aluno', 'pergunta'], name='resposta_unica')
        ]
    # Quero definir uma restrição de unicidade nos fields aluno e pergunta, e o nome dessa restrição é resposta_unica
