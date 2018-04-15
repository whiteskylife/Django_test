
from django import forms
from django.forms import fields
from django.forms import widgets
from app03 import models
from django.forms.models import ModelChoiceField,ModelMultipleChoiceField
from django.core.exceptions import ValidationError

class UserInfoForm(forms.Form):
    user = fields.CharField(
        required=False,
        widget=widgets.Textarea(attrs={'class': 'c1'})
    )

    pwd = fields.CharField(
        max_length=12,
        widget=widgets.PasswordInput(attrs={'class': 'c1'})
    )
# 针对两种select框创建方式分别实现动态select
    user_type = fields.ChoiceField(
        # choices=models.UserType.objects.values_list('id', 'name'),  # 构造方法中定义choices后，这里取的值没用了
        choices=[]
    )

    user_type2 = fields.CharField(
        widget=widgets.Select(choices=[])
    )

    user_type3 = ModelChoiceField(
        queryset=models.UserType.objects.all(),
        empty_label='请选择用户类型',
        to_field_name='id'      # HTML中select标签下option标签的value的值对应的字段
    )

    def __init__(self, *args, **kwargs):
        """
            重写父类构造方法，构造方法只有在创建类的实例的时候才会执行，
            利用构造方法的特性，实例化为对象时去数据库select可实现动态select获取，之后封装到对象中
        """
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = models.UserType.objects.values_list('id', 'name')     # 每次实例化为对象时都会去数据库中取数据
        self.fields['user_type2'].widget.choices = models.UserType.objects.values_list('id', 'name') # 针对两种select框创建方式分别实现动态select


class RegisterForm(forms.Form):

    user = fields.CharField(
        error_messages={'xxx': '用户名已存在'},
        min_length=2,
        required=False,
        label='用户名：',
        widget=widgets.TextInput(attrs={'class': 'c1'})
    )
    pwd = fields.CharField(
        max_length=12,
        label='密码：',
        widget=widgets.PasswordInput(attrs={'class': 'c1'})
    )



    def clean(self):
        """
        全局钩子函数clean，能拿到cleaned_data中所有验证通过的数据，对整体进行验证，可以进一步进行登录验证
        :return:
        """
        # c = models.User.objects.filter(user=self.cleaned_data['user'], pwd=self.cleaned_data['pwd']).count()
        # a = {'user': self.cleaned_data.get('user'), 'pwd': self.cleaned_data.get('pwd')}
        print(self.cleaned_data,'cleaned_data -----2222222222222222222222222')
        c = models.User.objects.filter(user=self.cleaned_data.get('user'), pwd=self.cleaned_data.get('pwd')).count()
        print(c, 'this is c---------')
        if c:
            return self.cleaned_data
        else:
            raise ValidationError('用户名或密码错误', code='xxx')

'''
小结：
form 验证流程：
1、前端提交数据到后台form
2、循环判断所有字段根据正则表达式（默认或自定义正则）
3、执行字段对应的钩子函数，再判断下一个字段（正则、钩子函数）
4、所有字段循环完毕，最后执行clean钩子函数、post钩子

客户端POST提交的数据作为我们自定义Form类的参数实例化的得到的form对象可以帮助我们进行表单验证，他验证的流程大致是这样的
    循环遍历用户提交的POST表单中的数据，取出存在于自定义的Form类中的字段，比如name，password。
    将取出的字段按照自定义的Form类中字段的验证规则（包括是否为空、长短、以及正则等）进行验证
    如果Form类中定义了钩子函数cleaned_字段名，就会调用钩子函数，对指定的字段进行更精细的验证（比如用户登陆）
'''
