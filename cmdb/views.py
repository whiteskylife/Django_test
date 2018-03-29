from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View  # CBV模式class需要继承这个View类

from django.core.files.uploadedfile import InMemoryUploadedFile # 上传文件用到的类


USER_LIST = [
    {'username': 'whisky', 'email': 'whisky@163.com', 'gender': 'male'}
]


# def login(request):
#     """
#     :param request:包含了用户端请求提交的所有的信息
#     :return:
#     """
#     # print(request.method)
#     error_msg = ''
#     if request.method == "POST":
#         user = request.POST.get('user', None)
#         pwd = request.POST.get('pwd', None)
#         if user == 'whisky' and pwd == '123':
#             return redirect('/home')  # 必须要加/,代表本地URL
#         else:
#             error_msg = "用户名或密码错误"
#     return render(request, 'login.html', {'error_msg': error_msg})


def home(request):
    if request.method == "POST":
        u = request.POST.get('username')
        e = request.POST.get('email')
        g = request.POST.get('gender')
        temp = {'username': u, 'email': e, 'gender': g}
        USER_LIST.append(temp)
    return render(request, 'home.html', {'user_list': USER_LIST})


def upload(request):
    import os
    if request.method == "POST":
        try:
            file_obj = request.FILES.get('upload_file')
            path = os.path.join('upload', file_obj.name)
            f = open(path, mode='wb')
            for content in file_obj.chunks():  # from django.core.files.uploadedfile import InMemoryUploadedFile # 上传文件用到的类中的chunks方法
                f.write(content)
            f.close()
        except Exception as e:
            print('提交为空')
    return render(request, 'home.html')


class Home(View):
    """
        Django的CBV模式
    """
    def dispatch(self, request, *args, **kwargs):
        '''
            调用父类的dispatch方法，再父类中dispatch方法利用反射区分处理用户提交时使用方法（POST，GET...）
        '''
        print('before')
        result = super(Home, self).dispatch(request, *args, **kwargs)
        print('after')
        return result

    def get(self, request):
        print(request.method, '-----------------------------------------')
        return render(request, 'home.html')  # 返回时，先返回给dispatch方法，由dispatch把html返回给用户

    def post(self, request):
        print(request.method, '-----------------------------------------')
        return render(request, 'home.html')


# USER_DICT = {
#     'k1': 'root1',
#     'k2': 'root2',
#     'k3': 'root3',
#     'k4': 'root4',
# }

USER_DICT = {
    '1': {'name': 'root1', 'email': 'root@live.com'},
    '2': {'name': 'root2', 'email': 'root@live.com'},
    '3': {'name': 'root3', 'email': 'root@live.com'},
    '4': {'name': 'root4', 'email': 'root@live.com'},
    '5': {'name': 'root5', 'email': 'root@live.com'},
}


def index(request):
    return render(request, 'index.html', {'user_dict': USER_DICT})


def index2(request, nid):
    # print(request.path_info)  # path_info方法：当前URL，可以直接传给前端
    from django.urls import reverse
    v = reverse('indexx', args=(666, ))
    # v = reverse('indexx', kwargs={'nid': 1, 'uid': '99'})
    print(v)
    # return render(request, 'index.html', {'user_dict': USER_DICT})
    return render(request, 'index.html', {'url': v})


def detail(request, nid, uid):
    # print(nid, uid)
    # return HttpResponse(nid)

    # nid = request.GET.get('nid')  # jango从urls.py 中取值无需再get('nid')
    detail_info = USER_DICT[nid]
    return render(request, 'detail.html', {'detail_info': detail_info})

'''
访问：http://127.0.0.1:8000/index
跳转：http://127.0.0.1:8000/detail-5-5.html

也可以用下面的**kwargs方式收参数
def detail(request, *args, **kwargs):

    detail_info = USER_DICT[kwargs['nid']]
    return render(request, 'detail.html', {'detail_info': detail_info})

'''


from cmdb import models         # 导入models

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


