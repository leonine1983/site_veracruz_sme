from django.contrib import admin
from django.urls import path
from dashboard.views import *
from django.contrib.auth import views as auth_views

app_name = 'painel'

urlpatterns = [
    path('/login', loginCreated, name='login'),
    path('logout/', user_logout, name='logout'),

    # Tipos publicação
    path('criar/tiposPublicacao/', TiposPublicacaoCreateView.as_view(), name='tiposPublicacao_create'),
    
    # Publicação
    path('/all', PublicacaoListView.as_view(), name='publicacao_list'),
    path('criar/', PublicacaoCreateView.as_view(), name='publicacao_create'),
    path('<int:pk>/editar/', PublicacaoUpdateView.as_view(), name='publicacao_edit'),
    path('<int:pk>/excluir/', PublicacaoDeleteView.as_view(), name='publicacao_delete'),

    # links
    path('/links', LinkListView.as_view(), name='link_list'),
    path('<int:pk>/', LinkDetailView.as_view(), name='link_detail'),
    path('novo/', LinkCreateView.as_view(), name='link_create'),
    path('/<int:pk>/editar/', LinkUpdateView.as_view(), name='link_update'),
    path('/<int:pk>/deletar/link', LinkDeleteView.as_view(), name='link_delete'),
    path('/<int:pk>/deletarLink/link', LinkDeleteViewPainel.as_view(), name='link_deletePainel')
]
