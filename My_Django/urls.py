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
from cmdb import views
from django.conf.urls import url, include
from app04 import views

urlpatterns = [
    url(r'cmdb/', include("app01.urls")),
    url(r'monitor/', include("app02.urls")),
    url(r'app03/', include("app03.urls")),
    path(r'article/', views.article),
    re_path(r'article-(?P<article_type_id>\d+)-(?P<category_id>\d+)', views.article),
]




# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path(r'h.html/', views.home),
#     # path(r'login', views.login),
#     # path(r'home', views.home),
#     path(r'upload', views.upload),
#     path(r'home', views.Home.as_view()),
#     path('index/', views.index),
#     # path(r'detail/', views.detail),
#     # re_path(r'detail-(\d+).html/', views.detail),
#     re_path(r'detail-(?P<nid>\d+)-(?P<uid>\d+).html/', views.detail),
#     re_path(r'asdasdasdasd/(?P<nid>\d+)/', views.index2, name='indexx'),
#     # url(r'cmdb/', include("app01.urls")),
#     re_path('orm/', views.orm),
# ]
