from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
# Create your views here.


def login(request):
    """
    :param request:包含了用户端请求提交的所有的信息
    :return:
    """
    # print(request.method)
    error_msg = ''
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()  # first直接取到对象
        if obj:
            return redirect('/cmdb/index/')         # 验证通过跳到后台
        else:
            return render(request, 'login.html')
    else:
        return redirect('/index/')
        # return render(request, 'login.html', {'error_msg': error_msg})


def index(request):
    return render(request, 'index.html')



def user_info(request):
    """
    用户列表打印、添加用户
    """
    if request.method == "GET":
        user_list = models.UserInfo.objects.all()                   # user_list是QuerySet类型，里面是包含结果的对象列表
        # print(user_list.query)                                      # 把orm语句翻译成SQL语句
        return render(request, 'user_info.html', {'user_list': user_list})
    elif request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        models.UserInfo.objects.create(username=u, password=p)
        # user_list = models.UserInfo.objects.all()
        # return render(request, 'user_info.html', {'user_list': user_list})
        return redirect('/cmdb/user_info/')           # 避免代码重复，这里用redirect方法，它是以get方法访问的


def user_detail(request, nid):
    obj = models.UserInfo.objects.filter(id=nid).first()  # 获取一条数据
    # models.UserInfo.objects.get(id=nid)   # 另外一种方法获取一条数据，如果数据库中没有对应id，程序直接报错，应该结合try使用
    print(obj)
    return render(request, 'user_detail.html', {'obj': obj})


def user_del(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/cmdb/user_info/')


def user_edit(request, nid):
    if request.method == 'GET':
        obj = models.UserInfo.objects.filter(id=nid).first()
        return render(request, 'user_edit.html', {'obj': obj})
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        models.UserInfo.objects.filter(id=nid).update(username=u, password=p)
        return redirect('/cmdb/user_info/')


from app01 import models         # 导入models


def orm(request):
    # 创建一条数据
    # 推荐方式一：
    # models.UserInfo.objects.create(username='root', password='123')  # UserInfo为表名

    # 第二种方式
    # dic = {'username': 'eric', 'password': '123'}
    # models.UserInfo.objects.create(**dic)

    # 第三种方式：
    # obj = models.UserInfo(username='alex', password='6666')
    # obj.save()


    # 查
    # result = models.UserInfo.objects.all()
    # result = models.UserInfo.objects.filter(username='root', password='123')
    # for row in result:
    #     print(row.id, row.username, row.password)
    # print(result)

    # 删除：
    # models.UserInfo.objects.filter(username='alex').delete()

    #  更新：
    # models.UserInfo.objects.filter(id=5).update(password='66666666666666666')

    return HttpResponse('orm')
