from django.urls import path

from quiz.main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('perguntas/<int:indice>', views.perguntas, name='perguntas'),  # int é o tipo do elemto presente depos do /
    # indice é nome do parametro
    path('classificacao/', views.classificacao, name='classificacao'),

]
