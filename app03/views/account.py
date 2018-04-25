from django.shortcuts import render,HttpResponse
from django import forms
from django.forms import fields
from django.forms import widgets
from app03 import models
import json


class LoginForm(forms.Form):
    username = fields.CharField()
    password = fields.CharField(
        max_length=64,
        min_length=12
    )

# import datetime
# from django.core import serializers
# def login(request):
#     ti = str(datetime.datetime.now())
#     ti1 = datetime.datetime.now()
#     data = serializers.serialize('json', ti1)
#     print(data, type(data))
#     ret = {'status':ti , 'error': None, 'data': None}
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     elif request.method == "POST":
#         obj = LoginForm(request.POST)
#         if obj.is_valid():
#             print(obj.cleaned_data)
#         else:
#             from django.forms.utils import ErrorDict
#             # print(obj.errors)             # 因为errors是字符串不是字典，无法通过json序列化为字符串
#             ret['error'] = obj.errors.as_json()   # 通过as_json把errors转换为字符串
#             # ret['error'] = obj.errors   # 通过as_json把errors转换为字符串
#     return HttpResponse(json.dumps(ret))

# 序列化错误信息：
# 前后台数据交互要通过字符串形式交互，Form中的error不是字符串，通过as_json把errors转换为字符串


class UserInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'


class UserInfoForm(forms.Form):
    username = fields.CharField(max_length=32)
    email = fields.EmailField()
    user_type = fields.ChoiceField(
        choices=models.UserType.objects.values('id', 'caption')
    )
    
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = models.UserType.objects.values_list('id', 'caption')


# def index(request):
#     if request.method == "GET":
#         obj = UserInfoModelForm()
#         return render(request, 'login.html', {'obj': obj})
#     elif request.method == "POST":
#         obj = UserInfoModelForm(request.POST)
#         obj.is_valid()
#         obj.save()
#         print(obj.cleaned_data)
#
#         # return HttpResponse
#         return render(request, 'login.html', {'obj': obj})



from app03.views.check_code import create_validate_code
from io import BytesIO


def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def index(request):
    if request.method == "GET":
        obj = UserInfoModelForm()
        return render(request, 'login.html', {'obj': obj})
    elif request.method == "POST":
        obj = UserInfoModelForm(request.POST)
        obj.is_valid()
        obj.save()
        print(obj.cleaned_data)

        # return HttpResponse
        return render(request, 'login.html', {'obj': obj})

