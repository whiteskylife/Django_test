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

