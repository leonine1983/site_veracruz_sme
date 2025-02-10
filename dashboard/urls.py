from django.contrib import admin
from django.urls import path
from dashboard.views import *

app_name = 'painel'

urlpatterns = [
    path('login', LoginSme.as_view(), name='login'),
    path('painel', Painel.as_view(), name='dashboard'),
    path('', PublicacaoListView.as_view(), name='publicacao_list'),
    path('criar/', PublicacaoCreateView.as_view(), name='publicacao_create'),
    path('<int:pk>/editar/', PublicacaoUpdateView.as_view(), name='publicacao_edit'),
    path('<int:pk>/excluir/', PublicacaoDeleteView.as_view(), name='publicacao_delete'),
]
