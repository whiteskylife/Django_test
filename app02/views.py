from django.shortcuts import render,HttpResponse
from app02 import models
from django.shortcuts import redirect
from utils import pagination
import json
# Create your views here.


def business(request):
    v1 = models.Business.objects.all()
    v2 = models.Business.objects.all().values('id', 'caption')       # values返回值不再是对象而是字典[{'id':1, "caption":"运维部"}...]
    v3 = models.Business.objects.all().values_list('id', 'caption')    # [(1, 运维部),(2, 开发)]

    return render(request, 'business.html', {'v1': v1, 'v2': v2, 'v3': v3})


# def host(request):
#     v1 = models.Host.objects.filter(nid__gt=0)
#     for row in v1:
#         print(row.nid, row.hostname, row.ip, row.port, row.b_id, row.b.caption, row.b.code, row.b.id, sep='\t')  #通过对象跨表操作直接用点即可
#
#     v2 = models.Host.objects.filter(nid__gt=0).values('nid', 'hostname', 'b_id', 'b__caption')      # 在models.Host.objects之后进行跨表时要用双下滑线，字符串的形式进行跨表操作
#     print(v2)       # 模板语言对于字典类型，前端取值只能通过点 . 来取值
#     # <QuerySet [{'b_id': 1, 'b__caption': '运维', 'hostname': 'c1.com', 'nid': 1},
#     # {'b_id': 1, 'b__caption': '运维', 'hostname': 'c2.com', 'nid': 2},
#     # {'b_id': 2, 'b__caption': '开发', 'hostname': 'c3', 'nid': 3}]>
#     for row in v2:
#         print(row['nid'], row['hostname'], row['b_id'], row['b__caption'])
#
#     v3 = models.Host.objects.filter(nid__gt=0).values_list('nid', 'hostname', 'b_id', 'b__caption')
#     print(v3)   # 模板语言对于元组类型，前端取值只能通过values_list中字符串顺序的索引来取值
#     # <QuerySet [(1, 'c1.com', 1, '运维'), (2, 'c2.com', 1, '运维'), (3, 'c3', 2, '开发')]>
#     for row in v3:
#         print(row[0], row[1], row[2], row[3])
#
#     return render(request, 'host.html', {'v1': v1, 'v2': v2, 'v3': v3})

def host(request):
    if request.method == "GET":
        v1 = models.Host.objects.filter(nid__gt=0)
        v2 = models.Host.objects.filter(nid__gt=0).values('nid', 'hostname', 'b_id', 'b__caption')      # 在models.Host.objects之后进行跨表时要用双下滑线，字符串的形式进行跨表操作
        v3 = models.Host.objects.filter(nid__gt=0).values_list('nid', 'hostname', 'b_id', 'b__caption')
        b_list = models.Business.objects.all()
        return render(request, 'host.html', {'v1': v1, 'v2': v2, 'v3': v3, 'b_list': b_list})

    elif request.method == "POST":
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        models.Host.objects.create(hostname=h,
                                   ip=i,
                                   port=p,
                                   b_id=b   # 或者这样写b=models.Business.objects.get(id=b)
                                   )

    return redirect('/monitor/host')


def test_ajax(request):
    import json
    ret = {'status': True, 'error': None, 'data':None}
    try:
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        if len(h) > 5:
            models.Host.objects.create(hostname=h,
                                       ip=i,
                                       port=p,
                                       b_id=b
                                       )
        else:
            ret['status'] = False
            ret['error'] = "太短了"
    except Exception as e:
        ret['status'] = False
        ret['error'] = '请求错误'

    return HttpResponse(json.dumps(ret))


def edit(request):
    try:
        nid = request.POST.get('nid')
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        p = request.POST.get('port')
        b = request.POST.get('b_id')
        models.Host.objects.filter(nid=nid).update(
            hostname=h,
            ip=i,
            port=p,
            b_id=b,
        )
    except Exception as e:
        return HttpResponse('输入错误')
    else:
        return HttpResponse('OK')


def app(request):
    if request.method == "GET":
        app_list = models.Application.objects.all()
        # for row in app_list:
        #     print(row.name, row.r.all())

        host_list = models.Host.objects.all()
        return render(request, 'app.html', {'app_list': app_list, 'host_list': host_list})
    elif request.method == "POST":
        app_name = request.POST.get('app_name')
        host_list = request.POST.getlist('host_list')
        # print(app_name, host_list)

        obj = models.Application.objects.create(name=app_name)
        obj.r.add(*host_list)
        return redirect('/monitor/app')


def ajax_add_app(request):
    ret = {'status': True, 'error': None, 'data': None}
    app_name = request.POST.get('app_name')
    # print(request.POST.get('host_list'))        # 前端如果传过来列表只能拿到最后一个元素
    host_list = request.POST.getlist('host_list')
    obj = models.Application.objects.create(name=app_name)
    obj.r.add(*host_list)           # 利用name=app_name的obj对象，添加对应主机，注意添加方式
    return HttpResponse(json.dumps(ret))  # HttpResponse只能传输字符串，这里需要把字典转换为字符串


def edit_ajax_app(request):
    app_name = request.POST.get('edit_app_name')
    aid = request.POST.get('aid')
    hid_list = request.POST.getlist('hid_list')
    print(aid, app_name, hid_list)  # c1111 ['2', '3']
    obj = models.Application.objects.get(id=aid)            # 更新Application应用表
    obj.name = app_name                                     # 更新Application应用表
    obj.save()                                              # 更新Application应用表
    obj.r.set(hid_list)                                     # 更新关系表
    return HttpResponse('OK')


def clear(request):
    obj = models.Application.objects.get(id=1)
    obj.r.clear()
    return HttpResponse('1111111111111')


from django.utils.safestring import mark_safe



class Page:
    def __init__(self, current_page, data_count, per_page_count=10, display_total_page=12):
        """
        :param current_page:        当前页
        :param data_count:          数据总量，数据总个数
        :param per_page_count:      每页显示数据条数
        :param display_total_page:  需要展示多少个页码,注意这里只能放偶数，奇数会有bug
        """
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.display_total_page = display_total_page
    @property
    def start(self):
        """
        :return: 根据当前页和每页显示的数据量生成每页起始数据索引，默认第一页为0
        """
        return (self.current_page - 1) * self.per_page_count
    @property
    def end(self):
        """
        :return: 根据当前页和每页显示的数据量生成每页末尾数据索引，默认第一页为10
        """
        return self.current_page * self.per_page_count
    @property
    def all_count(self):
        """
        根据数据总量、per_page_count计算总页数
        :return:总页数
        """
        count, surplus = divmod(self.data_count, self.per_page_count)  # count:总页数
        if surplus:
            count += 1  # 如果有剩余数据，页数 + 1
        return count

    def page_str(self, base_url):
        """
        :param base_url: 当前URL前缀，要加'/'
        :return: html字符串
        """
        # 生成html页码
        page_list = []
        if self.current_page > self.display_total_page / 2:  # 如果当前页大于5 而且当前页+5还在总页数之内
            start_display_page = self.current_page - self.display_total_page / 2  # 如果当前页数为6，从第1页开始展示
        else:
            start_display_page = 1

        stop_display_page = start_display_page + self.display_total_page - 1
        if stop_display_page > self.all_count:
            stop_display_page = self.all_count
            start_display_page = stop_display_page - self.display_total_page + 1
            if start_display_page < 1:
                start_display_page = 1

        if self.current_page == 1:
            pre = '<a class="page" href="javascript:void(0);">上一页</a>'
        else:
            pre = '<a class="page" href="%s?p=%s">上一页</a>' % (base_url, self.current_page - 1)
        page_list.append(pre)
        for i in range(int(start_display_page), int(stop_display_page) + 1):  # for循环生成页码，不包含下边界所以+1
            if i == self.current_page:
                temp = '<a class="page active" href="%s?p=%s">%s</a>' % (base_url, i, i)
            else:
                temp = '<a class="page" href="%s?p=%s">%s</a>' % (base_url, i, i)
            page_list.append(temp)

        if self.current_page == self.all_count:
            next_page = '<a class="page" href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a class="page" href="%s?p=%s">下一页</a>' % (base_url, self.current_page + 1)
        page_list.append(next_page)

        jump = """
           <input type='text'/><a onclick='jumpTo(this, "%s?p=");'>GO</a>
           <script>
               function jumpTo(ths,base){
                   var val = ths.previousSibling.value;
                   location.href = base + val;
               }
           </script>

           """ % base_url
        page_list.append(jump)
        # 生成html转换为字符串
        page_str = " ".join(page_list)
        return page_str


LIST = []
for num in range(1, 198):
    LIST.append(num)


def user_list(request):
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count', 10)     # 基于cookie实现动态指定每页显示多少条数据
    val = int(val)
    # page_obj = pagination.Page(current_page, len(LIST))
    page_obj = Page(current_page, len(LIST), val)
    data = LIST[page_obj.start:page_obj.end]                       # 每页对应需要显示的数据，由列表切片来取出数据给前端展示
    page_str = page_obj.page_str("/monitor/user_list/")
    return render(request, 'user_list.html', {'li': data, 'page_str': page_str})


user_info = {
    'whisky': {'pwd': '123'},
    'sky': {'pwd': '123'},
}


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        dic = user_info.get(u)
        if not dic:
            return render(request, 'login.html')
        if dic['pwd'] == p:
            res = redirect('/monitor/index/')
            import datetime
            current_date = datetime.datetime.utcnow()
            current_date = current_date + datetime.timedelta(seconds=5)  # 设置cookie根据当前时间延迟5秒后过期
            res.set_cookie('username111', u, expires=current_date)
            return res
        else:
            return render(request, 'login.html')


def auth(func):
    def inner(request, *args, **kwargs):
        v = request.COOKIES.get('username111')
        if not v:
            return redirect('/monitor/login/')
        ret = func(request, *args, **kwargs)
        return ret
    return inner


# -----------FBV装饰器--------------------------------
@auth
def index(request):
    v = request.COOKIES.get('username111')      # 获取当前已经登录用户的cookie，cookie的key为：username111，value为whisky
    return render(request, 'index.html', {'current_user': v})


def cookie(request):
    v = request.COOKIES['username111']         # 用户发数据携带的cookie，是一个字典
    return HttpResponse(v)


# --------- CBV装饰器 --------------
from django import views

# 导入jango的method_decorator方法实现类的装饰器
from django.utils.decorators import method_decorator


# class Order(views.View):
#     @method_decorator(auth)         # 借助Django的方法实现类中的装饰器
#     def get(self, request):
#         v = request.COOKIES.get('username111')
#         if not v:
#             return redirect('/monitor/login/')
#         return render(request, 'index.html', {'current_user': v})
#     @method_decorator(auth)
#     def post(self, request):
#         v = request.COOKIES.get('username111')
#         return render(request, 'index.html', {'current_user': v})

@method_decorator(auth, name='dispatch')  # 直接装饰类，不用写装饰dispatch了
class Order(views.View):

    # @method_decorator(auth)                       # 可以直接装饰类，就不用再重写dispatch
    # def dispatch(self, request, *args, **kwargs):
    #     return super(Order, self).dispatch(request, *args, **kwargs)

    # @method_decorator(auth)         # 借助Django的方法实现类中的装饰器, 可以直接在dispatch方法上加装饰器，下面的所有方法就都被装饰了
    def get(self, request):
        v = request.COOKIES.get('username111')
        if not v:
            return redirect('/monitor/login/')
        return render(request, 'index.html', {'current_user': v})

    def post(self, request):
        v = request.COOKIES.get('username111')
        return render(request, 'index.html', {'current_user': v})








