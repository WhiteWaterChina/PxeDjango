# -*- coding:cp936 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


os_type_list = ["redhat","centos", "suse", "ubuntu", "windows"]
os_version_list = []


def index(request):
    return  render(request, "pxe/html.html", {'os_type_list': os_type_list})


def get_os_verison(request):
    if request.method == "POST":
        os_version = request.POST.get('os_type', '')
        if os_version == 'redhat':
            os_version_list = ['6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7.0', '7.1', '7.2', '7.3', '7.4']
        elif os_version == 'centos':
            os_version_list = ['6.4', '6.5', '6.6', '6.7', '6.8', '6.9', '7.0', '7.1', '7.2', '7.3', '7.4']
        elif os_version == 'suse':
            os_version_list = ['11.2', '11.3', '11.4', '12.0', '12.1', '12.2', '12.3']
        elif os_version == 'ubuntu':
            os_version_list = ['14.04.5', '16.10', '17.04', '17.10']
        elif os_version == 'windows':
            os_version_list = ['2016-datacenter-cn', '2016-datacenter-en', '2016-standard-en', '2016-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn', '2012r2-standard-cn']
        else:
            os_version_list = ['None']
    os_type_list_temp = []
    os_type_list_temp.append(os_version)
    return  render(request, "pxe/get_os_version.html", {'os_type_list':os_type_list_temp, 'os_version_list':os_version_list})

