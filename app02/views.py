from django.shortcuts import render,HttpResponse
from app02 import models
from django.shortcuts import redirect
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