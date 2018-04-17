from django.shortcuts import render,HttpResponse
from django import forms
from django.forms import fields
from django.forms import widgets
import json

class LoginForm(forms.Form):
    username = fields.CharField()
    password = fields.CharField(
        max_length=64,
        min_length=12
    )


def login(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == "POST":
        obj = LoginForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
        else:
            from django.forms.utils import ErrorDict
            # print(obj.errors)             # 因为errors是字符串不是字典，无法通过json序列化为字符串
            # ret['error'] = obj.errors.as_json()   # 通过as_json把errors转换为字符串
            ret['error'] = obj.errors   # 通过as_json把errors转换为字符串
    return HttpResponse(json.dumps(ret))

