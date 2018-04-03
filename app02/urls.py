"""My_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app02 import views
from django.conf.urls import url, include


urlpatterns = [
    # url(r'login/', views.login),
    # re_path('orm/', views.orm),
    re_path(r'^business$', views.business),    # 不加$符号，后面business_add这样的URL都不生效
    re_path(r'^host$', views.host),
    re_path(r'^test_ajax$', views.test_ajax),
    re_path(r'^edit', views.edit),
]



