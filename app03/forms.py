
from django import forms
from django.forms import fields
from django.forms import widgets


class UserInfoForm(forms.Form):
    user = fields.CharField()