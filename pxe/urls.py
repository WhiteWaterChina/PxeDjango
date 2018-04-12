# -*- coding:cp936 -*-

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

app_name = 'pxe'

urlpatterns = [
    path('', views.index, name='index'),
    path('pxe', views.get_os_verison, name='get_os_version'),

]
