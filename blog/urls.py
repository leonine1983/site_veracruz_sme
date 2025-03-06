from django.contrib import admin
from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog, name='home'),
    path('/<int:pk>', visualizaPost, name='visualizaPost'),    
    path('/curtir/<int:pk>', curtidaPost, name='curtiPost'),


]
