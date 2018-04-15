from django.shortcuts import render,HttpResponse,redirect
from app03 import models

# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'root' and pwd == '123':
            # 1.后台生成随机字符串
            # 2.用户请求过来，写到用户浏览器cookie中，cookie的key默认为“sessionid”，value为随机字符串
            # 3.在随机字符串对应的字典中设置响应的内容
            # 4.保存session到数据库的session表中（session中设置值，Django自动写到数据库session表中）
            # 应用session之前同步数据库：python3 manage.py makemigrations  python3 manage.py migrate
            request.session['username'] = user
            request.session['is_login'] = True

            if request.POST.get('rmb', None) == '1':
                request.session.set_expiry(10)  # 手动设置超时时间：10s
            return redirect('/app03/index/')
        else:
            return render(request, 'login.html')


# def index(request):
#     # request.session:获取值->jango内部操作：获取当前用户的随机字符串，根据随机字符串获取对应信息
#     # if request.session['is_login']:   # session不存在会报错
#     if request.session.get('is_login', None):
#         # return HttpResponse('session --OK')
#         # return HttpResponse(request.session['username'])
#         return render(request, 'index.html')
#     else:
#         return HttpResponse('out!')


def logout(request):
    request.session.clear()           # 注销时用，数据库中不会清除
    # request.session.clear_expired()  数据库中彻底清除除session
    return redirect('/app03/login/')


def index(request):
    return render(request, 'csrf.html')


def csrf(request):
    if request.POST.get('user') == 'root' and request.POST.get('pwd') == '123':
        return HttpResponse('OK-----------------!')
    else:
        return HttpResponse('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

class Foo:
    def render(self):
        return HttpResponse('OK')


def test(request):
    print('in test Middle view')
    return Foo()


from django.views.decorators.cache import cache_page


# @cache_page(10)             # 10s缓存时间
def cache(request):
    import time
    ctime = time.time()
    return render(request, 'cache.html', {'ctime': ctime})


def signal(request):

    from sg import custom_signal_name  # 导入自定义信号

    custom_signal_name.send(sender='asdasd', aaa=123, bbb=456)

    return HttpResponse('this is a test for Django-signal ')



# -------------------FORM------------------------


from django import forms
from django.forms import widgets    # widgets插件相关功能,包括了HTMl中INPUT、select、checkbox、radio等等全部标签
from django.forms import fields     # fields:字段相关功能


class FM(forms.Form):
    """
        下面的所有字段名字必须和前端的变量name的值相同，否则拿不到值
        字段本身只用作验证的功能，fields负责生成HTML
    """
    user = fields.CharField(
        error_messages={'required': '用户名不能为空.'},
        widget=widgets.Textarea(attrs={'class': 'c1'}),     # widget设置表单字段在html页面的类型,attrs给表单标签设置属性
        label='用户名',
        initial='root',
        help_text='请输入用户名(手机号、邮箱)'
    )

    pwd = fields.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'c2'}),
        label='密码',
    )
    email = fields.EmailField(error_messages={'required': '邮箱不能为空.', 'invalid': '邮箱格式错误'})  # 自定义错误信息

    f = fields.FileField()

    city = fields.ChoiceField(
        choices=[(0, '上海'), (1, '北京'), (2, '东莞')]
    )
    city1 = fields.MultipleChoiceField(
        choices=[(0, '上海'), (1, '北京'), (2, '东莞')]
    )


def fm(request):
    if request.method == "GET":
        '''
        打开一个新的编辑页面把默认值都获取到：创建个字典，把类中的字段一一写为字典的key，字典的值即为默认值，可以通过models从数据库获取
        传递对象到前端时加上initial=dic参数即可设置默认值
        注意：字段名必须和自定义类中的字段一一对应
        '''
        dic = {
            'user': 'r1',
            'pwd': '123123',
            'email': 'asd@asd',
            'city1': 1,
            'city2': [1, 2],
        }
        obj = FM(initial=dic)
        return render(request, 'fm.html', {'obj': obj})  # 打开页面，并将表单验证类对象传到html生成表单标签，利用表单类自动创建表单标签
    elif request.method == "POST":
        obj = FM(request.POST)                   # 创建验证表单类，将用户请求POST对象传进Form类中进行表单验证
        r1 = obj.is_valid()                      # is_valid方法：对form中每一个字段逐一进行验证,返回验证是否通过的布尔值
        if r1:
            print(obj.cleaned_data)                         # 以字典的形式返回正确信息
            models.UserInf.objects.create(**obj.cleaned_data) # 利用cleaned_data实现注册
        else:
            # print(obj.errors.as_json())
            # print(obj.errors['user'])       # errors方法包含了所有的错误信息,取值通过字典方式
            print(obj.errors)
        return render(request, 'fm.html', {'obj': obj})

'''
class UserInfoForm(forms.Form):
    user = fields.CharField(
        required=False,
        widget=widgets.Textarea(attrs={'class': 'c1'})
    )

    pwd = fields.CharField(
        max_length=12,
        widget=widgets.PasswordInput(attrs={'class': 'c1'})
    )

    user_type = fields.ChoiceField(
        # choices=[(1, '普通用户'), (2, '超级用户')],
        choices=models.UserType.objects.values_list('id', 'name'),
    )

    user_type2 = fields.CharField(
        # widget=widgets.Select(choices=[(0, '上海'), (1, '北京'), (2, '东莞')])
        widget=widgets.Select(choices=models.UserType.objects.values_list('id', 'name'))
    )

    user_type3 = fields.MultipleChoiceField(
        # choices=[(1, '普通用户'), (2, '超级用户')],
        choices=models.UserType.objects.values_list('id', 'name'),
    )

    user_type4 = fields.CharField(
        # widget=widgets.SelectMultiple(choices=[(0, '上海'), (1, '北京'), (2, '东莞')])
        widget=widgets.SelectMultiple(choices=models.UserType.objects.values_list('id', 'name'))
    )

'''
'''
def test1(request):

    users = models.User.objects.all()
    for row in users:
        print(row.user, row.pwd, row.ut_id)
        print(row.ut.name)   # 再发起一次SQL请求，如果有10个用户，每次循环执行一次跨表操作，整个循环将发起11次SQL请求

    users = models.User.objects.all().values('user', 'pwd', 'ut__name')
    for row in users:            # 这种方式跨表只发起一次SQL请求，单反回的非queryset对象，而是字典
        print(row.user, row.pwd, row.ut_id)

    users = models.User.objects.all().select_related('ut')      # 一次性把关联的ut表数据取过来再进行操作，其他的关联表都不取，不加参数默认取所有关联的表的数据
    for row in users:
        print(row.user, row.pwd, row.ut_id)
        print(row.ut.name)                                   # 如果有10个用户，整个循环将发起1次SQL请求


# prefetch_related
    users = models.User.objects.filter(id__gt=30).prefetch_related('ut')      # 一次取到所有关联表数据
    # prefetch 将做两步操作：
    # select * from users where id > 30
    # jango获取上一条SQL所有的ut_id,假设ut_id=[1, 2]
    # select * from user_type where id in [1,2]

    for row in users:
        print(row.user, row.pwd, row.ut_id)
        print(row.ut.name)                                   # 如果有10个用户，整个循环将发起1次SQL请求
'''

from app03.forms import UserInfoForm


def form(request):
    if request.method == "GET":
        obj = UserInfoForm({'user_type': '2'})
        # obj.fields['user_type'].choices = models.UserType.objects.values_list('id', 'name')
        # print(obj.fields)
        # print(models.UserType.objects.values_list('id', 'name'),)
        return render(request, 'index.html', {'obj': obj})


from app03.forms import RegisterForm


#
def register(request):
    if request.method == "GET":
        obj = RegisterForm()
        return render(request, 'index.html', {'obj': obj})
    elif request.method == "POST":
        obj = RegisterForm(request.POST, initial={'user': request.POST.get('user')})     # 提交验证失败保留用户名
        obj.is_valid()
        print(obj.errors)
        return render(request, 'index.html', {'obj': obj})




from django.core.exceptions import NON_FIELD_ERRORS
'''
 {
    '__all__':[],    # 整体验证clean方法的错误信息放在这里 , 也可以写成NON_FIELD_ERRORS(点击看源码可知代指字符串__all__)
     "email": [{"code": "required", "message": "This field is required."}],
  "user": [{"code": "required", "message": "This field is required."}],
  "pwd": [{"code": "required", "message": "This field is required."}]
  }
'''
