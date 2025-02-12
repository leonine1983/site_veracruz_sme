from django.contrib import admin
from django.urls import path
from dashboard.views import *
from django.contrib.auth import views as auth_views

app_name = 'painel'

urlpatterns = [
    path('/login', loginCreated, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', PublicacaoListView.as_view(), name='publicacao_list'),
    path('criar/', PublicacaoCreateView.as_view(), name='publicacao_create'),
    path('<int:pk>/editar/', PublicacaoUpdateView.as_view(), name='publicacao_edit'),
    path('<int:pk>/excluir/', PublicacaoDeleteView.as_view(), name='publicacao_delete'),
]
