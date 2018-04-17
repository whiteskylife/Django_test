from django.shortcuts import render,HttpResponse,redirect
from app03 import models
# Create your views here.
from django.db.models import Count, Avg, Max, Min, Sum

def login(request):
    """
    # if request.method == "GET":
    #     return render(request, 'login.html')
    # elif request.method == "POST":
    #     user = request.POST.get('user')
    #     pwd = request.POST.get('pwd')
    #     if user == 'root' and pwd == '123':
    #         # 1.后台生成随机字符串
    #         # 2.用户请求过来，写到用户浏览器cookie中，cookie的key默认为“sessionid”，value为随机字符串
    #         # 3.在随机字符串对应的字典中设置响应的内容
    #         # 4.保存session到数据库的session表中（session中设置值，Django自动写到数据库session表中）
    #         # 应用session之前同步数据库：python3 manage.py makemigrations  python3 manage.py migrate
    #         request.session['username'] = user
    #         request.session['is_login'] = True
    #
    #         if request.POST.get('rmb', None) == '1':
    #             request.session.set_expiry(10)  # 手动设置超时时间：10s
    #         return redirect('/app03/index/')
    #     else:
    #         return render(request, 'login.html')
    # a = models.User.objects.filter(user='root').update(pwd='66666666')
    # a = models.User.objects.all()
    # a = models.User.objects.get(id='5')
    # a = models.Book.objects.filter(author='yuan').values('name', 'price')
    # a = models.Book.objects.filter(author='yuan').values_list('name', 'price')
    # a = models.Book.objects.exclude(author='yuan')
    # for item in a:
    #     print(item.name, item.price, item.pub_date, item.author)
    # a = models.Book.objects.all().values('name').distinct().count()
    # a = models.Book.objects.all().values('name').distinct()

# 一对多
# 添加数据
    # 方式一：
    # models.Book.objects.create(name='Linux', price=77, pub_date='2017-12-12', publish_id=2)

    # 方式二(通过对象方式)：
    # publish_obj = models.Publish.objects.filter(name='人民出版社')[0]
    # models.Book.objects.create(name='Linux', price=77, pub_date='2017-12-12', publish=publish_obj)
        # 把publish_obj对象赋值给Book类中的publish，内部会把"人民出版社"的id赋值给外键关联的publish_id

# 查询：
    # 需求：查询python书籍对应的出版社名字和城市都拿到（正向查询）
    # 方式一（双下划线正向跨表）：
    #     r = models.Book.objects.filter(name='python').values('publish__name', 'publish__city')

            # 补充（双下划线反向跨表查询,这里不是对象的反向跨表，不用_set方式）
            # a = models.Publish.objects.filter(book__name="python").values("name")
            # print(a)         # <QuerySet [{'name': '人民出版社'}]>

    # 方式二(通过对象方式)：
    #     book_obj = models.Book.objects.get(name='python')
    #     name = models.Book.objects.get(name='python').publish      # 一对多的查询，models.Book.objects.get(name='python').publish  结果是一定是一个对象
    #     city = models.Book.objects.get(name='python').publish.city
    #     print(name, city)                                                # 输出 Publish object (3) 南京

    # 需求：查询人民出版社出了哪些书（反向查询）
    # 方式一（双下划线跨表）：
    #     obj = models.Book.objects.filter(publish__name='人民出版社').values("name", "price")
    #     print(obj)  # <QuerySet [{'price': 89, 'name': 'python'}, {'price': 77, 'name': 'JAVA'}]>
    # 方式二(通过对象方式)：
    #     pub_obj = models.Publish.objects.filter(name="人民出版社")[0]
    #     ret = models.Book.objects.filter(publish=pub_obj).values("name", "price")

    # 方式三（反向查找，通过表名_set）：
    # a = models.Publish.objects.filter(name="人民出版社")[0].book_set.values("name", "price")
    # a = models.Publish.objects.get(name="人民出版社").book_set.values("name", "price")       # 注意对别get和filter查询写法上的区别
    #     print(a)    # <QuerySet [{'price': 89, 'name': 'python'}, {'price': 77, 'name': 'JAVA'}]>
    # 小结：三种方式内部都是利用ForeignKey来实现的


    # 需求：查询在北京的出版社出版的所有书
    # 错误思路：a = models.Publish.objects.filter(city="北京").values("id")
    #           b = models.Book.objects.filter(publish_id=a).values("name")
    # 正确思路：
    # 方式一（正向查询，双下滑线跨表）：
    # a = models.Book.objects.filter(publish__city="北京").values("name")
    # print(a)  # <QuerySet [{'name': 'python'}, {'name': 'Linux'}, {'name': 'GO'}]>

    # 方式二（反向查询，双下滑线跨表）
    # b = models.Publish.objects.filter(city="北京").values("book__name")
    # print(b)  # <QuerySet [{'book__name': 'python'}, {'book__name': 'Linux'}, {'book__name': 'GO'}]>

    # 方式二（反向查询，_set跨表）
    # c = models.Publish.objects.filter(city="北京")
    # d = []
    # for i in c:
    #     d.append(i.book_set.values("name"))
    # print(d)    # [<QuerySet [{'name': 'python'}]>, <QuerySet [{'name': 'Linux'}, {'name': 'GO'}]>]
    '''
 '''


    # 多对多：
    # 查询：
    # 需求：查询书名是Linux的作者名字
        a = models.Book.objects.get(name='Linux').authors.all()
        print(a)        # <QuerySet [<Author: alex>, <Author: yuan>]> , all()结果models类中需要加上__str__方法
 """

    # 需求：找出yuan作者写过的书：
    # 错误写法：a = models.Author.objects.filter(name='yuan').book_set.values("name")  # filter反向查询_set跨表时不能用在filter后面，filter结果是多个QuerySet对象
    # 方式一：_set反向跨表查询
    # a = models.Author.objects.get(name='yuan').book_set.values("name")
    # print(a)
    # 方式二：双下划线正向跨表查询
    # a = models.Book.objects.filter(authors__name='yuan').values("name")
    # print(a)

    return HttpResponse('ooo')

