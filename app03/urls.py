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
from app03.views import test
from app03.views import account
from django.conf.urls import url, include


urlpatterns = [
    # re_path(r'^login.html$', account.login),
    re_path(r'^test$', test.login),
    re_path(r'^index.html$', account.index),
    re_path(r'^check_code.html$', account.check_code),
    # re_path(r'^index/', test.index),
    # re_path(r'^logout/$', test.logout),
    # re_path(r'^csrf/$', test.csrf),
    # re_path(r'^test/$', test.test),
    # re_path(r'^cache/$', test.cache),
    # re_path(r'^signal/$', test.signal),
    # re_path(r'^fm/$', test.fm),
    # re_path(r'^form/$', test.form),
    # re_path(r'^register/$', test.register),
]


