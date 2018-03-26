from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

USER_LIST = [
    {'username': 'whisky', 'email': 'whisky@163.com', 'gender': 'male'}
]


def login(request):
    """
    :param request:包含了用户端请求提交的所有的信息
    :return:
    """
    # print(request.method)
    error_msg = ''
    if request.method == "POST":
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        if user == 'whisky' and pwd == '123':
            return redirect('/home')
        else:
            error_msg = "用户名或密码错误"
    return render(request, 'login.html', {'error_msg': error_msg})


def home(request):
    if request.method == "POST":
        u = request.POST.get('username')
        e = request.POST.get('email')
        g = request.POST.get('gender')
        temp = {'username': u, 'email': e, 'gender': g}
        USER_LIST.append(temp)
    return render(request, 'home.html', {'user_list': USER_LIST})

# def home(request):
#     return HttpResponse('<h1>CMDB</h1>')
