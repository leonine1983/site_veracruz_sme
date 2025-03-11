from django.contrib import admin
from django.urls import path
from blog.views import *
from .models import TipoPublicacao

app_name = 'blog'

urlpatterns = [
    path('', blog, name='home'),
    path('/<int:pk>', visualizaPost, name='visualizaPost'),    
    path('/menu/<int:pk>', visualizaTipos, name='visualizaMenu'),    
    path('/curtir/<int:pk>', curtidaPost, name='curtiPost'),
    path('/coment/<int:pk>', comentPost, name='comentPost'),
    


]
