from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


def login(request):
    """
    :param request:包含了用户端请求提交的所有的信息
    :return:
    """
    # print(request.method)
    error_msg = ''
    user = request.POST.get('user', None)
    pwd = request.POST.get('pwd', None)
    if user == 'whisky' and pwd == '123':
        return redirect('http://www.baidu.com')
    else:
        error_msg = '用户名密码错误！'
    return render(request, 'login.html', {'error_msg': error_msg})


def home(request):
    return HttpResponse('<h1>CMDB</h1>')
