# -*- coding:cp936 -*-

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

app_name = 'pxe'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-os-version', views.config_pxe, name='get_os_version'),
    path('search', views.search, name='search'),
    path('set_pxe_reboot', views.set_pxe_reboot, name='set_pxe_reboot'),

]
