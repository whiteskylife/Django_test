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


class FM(forms.Form):
    """
        下面的所有字段名字必须和前端的变量name的值相同，否则拿不到值
        字段本身只用作验证的功能，fields负责生成HTML
    """
    user = forms.CharField(error_messages={'required': '用户名不能为空.'})
    pwd = forms.CharField(
        max_length=12,
        min_length=6,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'}
    )
    email = forms.EmailField(error_messages={'required': '邮箱不能为空.', 'invalid': '邮箱格式错误'})


def fm(request):
    if request.method == "GET":
        obj = FM()
        ret = models.User.objects.defer('user')
        ret1 = models.User.objects.all()
        print(ret,'------',ret1)
        return render(request, 'fm.html', {'obj': obj})
    elif request.method == "POST":
        obj = FM(request.POST)
        r1 = obj.is_valid()     # is_valid方法：对form中每一个字段逐一进行验证
        if r1:
            print(obj.cleaned_data)
        else:
            # print(obj.errors.as_json())
            # print(obj.errors['user'])       # errors方法包含了所有的错误信息,取值通过字典方式
            print(obj.errors)
        return render(request, 'fm.html', {'obj': obj})





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