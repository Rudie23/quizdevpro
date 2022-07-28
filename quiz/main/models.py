from django.db import models


# Create your models here.

# mvt (model view template)

class Pergunta(models.Model):
    enunciado = models.TextField()
    alternativas = models.JSONField()  # modelo permite ter uma hierarquia que permite colocar várias opções
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
