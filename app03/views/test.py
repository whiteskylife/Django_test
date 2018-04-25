from django.shortcuts import render, HttpResponse, redirect
from app03 import models
from app03.models import *
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


        # 需求：找出yuan作者写过的书：
        # 错误写法：a = models.Author.objects.filter(name='yuan').book_set.values("name")  # filter反向查询_set跨表时不能用在filter后面，filter结果是多个QuerySet对象
        # 方式一：_set反向跨表查询
            a = models.Author.objects.get(name='yuan').book_set.values("name")
            print(a)
        # 方式二：双下划线正向跨表查询
            a = models.Book.objects.filter(authors__name='yuan').values("name")
        # print(a)

    # 添加：
        # 需求：添加一个作者yuan到书名为GO的书
            autho_obj = models.Author.objects.get(name="yuan")
            models.Book.objects.get(name="GO").authors.add(autho_obj)

        # 需求：多对多操作更改书名为GO的书的作者为所有人：
            b = models.Author.objects.all()
            a = models.Book.objects.get(name="GO").authors.add(*b)
            print(a)

    # 删除
        # 需求：删除GO书的所有作者：
            # author_obj = models.Author.objects.all()
            # models.Book.objects.get(name="GO").authors.remove(*author_obj)
            # print(author_obj)

        # 需求：删除GO书的yuan作者
        #     方式1：models.Book.objects.get(name="GO").authors.remove(models.Author.objects.get(name="yuan")) # 通过对象绑定来建立关系
        #     方式二：models.Book.objects.get(name="GO").authors.remove(2)


    # 自行创建第三张表
    # 添加数据：models.Book_Author.objects.create(book_id=2, author_id=3)
        # 需求：查询书名为python的作者,通过对象方式，反向跨表_set
                #book_obj = models.Book.objects.get(name='python')
                #a = book_obj.book_author_set.values("author__name")

        # 需求：查找作者alex出过的书籍和价格
        # 方式一：
        #     a = models.Author.objects.get(name='alex').book_author_set.values("book__name", "book__price")
        #     print(a)  # <QuerySet [{'book__price': 77, 'book__name': 'Linux运维'}, {'book__price': 77, 'book__name': 'GO'}]>
        # 方式二：通过自建第三张表查询（不推荐）
        #     a = models.Book.objects.filter(book_author__author__name="alex").values('name', 'price')
        #     print(a) # <QuerySet [{'price': 77, 'name': 'Linux运维'}, {'price': 77, 'name': 'GO'}]>

        # 方式三：利用ManyToManyField字段跨表查询
        #     a = models.Book.objects.filter(authors__name='alex').values('name', 'price')
        #     print(a)


    # 分组聚合查询

    #聚合查询
    # 求出所有书籍的平均价格
    #     a = models.Book.objects.all().aggregate(Avg('price'))
    #     b = models.Book.objects.all().aggregate(Sum('price'))
    # 求出alex写的书籍的总价格
    #     c = models.Book.objects.filter(authors__name='alex').aggregate(alex_money=Sum('price'))  # alex_money设置查询结果字段的名字
    #     print(c)

    #分组查询：
    # 求出每一个作者出的全部书的价格和
    #     ret = models.Book.objects.values("authors__name").annotate(Sum('price'))
    #                   values:按照authors__name进行分组；annotate用来分组，Sum对分组后每一个组进行求和
    #     print(ret)

    # 查询各个出版社最便宜的书籍价格
        # a = models.Publish.objects.values("name").annotate(Min('book__price'))
        # print(a)


    # F 使用查询条件的值,专门取对象中某列值的操作
    from django.db.models import F,Q
    # 所有书籍价格+10
    # models.Book.objects.all().update(price=F('price')+10)

    # Q 构建搜索条件

    a = models.Book.objects.filter(Q(price=97) | Q(name='GO'))      # 或
    b = models.Book.objects.filter(~Q(name='GO'))                   # 非
    c = models.Book.objects.filter(Q(name__contains="G"))

    # Q查询结合关键字查询，Q查询要放在前
    d = models.Book.objects.filter(Q(name='GO'), price=97).iterator()
    print(d)

    # citys = City.objects.all()
    # for c in citys:
    #     print(c.province)
# 执行的SQL查询：
#     SELECT `app03_city`.`id`, `app03_city`.`name`, `app03_city`.`province_id` FROM `app03_city
#     SELECT `app03_province`.`id`, `app03_province`.`name` FROM `app03_province` WHERE `app03_province`.`id` = 1
#     SELECT `app03_province`.`id`, `app03_province`.`name` FROM `app03_province` WHERE `app03_province`.`id` = 1
#     SELECT `app03_province`.`id`, `app03_province`.`name` FROM `app03_province` WHERE `app03_province`.`id` = 2

# 如果使用select_related()函数：
#     citys_select_related = City.objects.all().select_related()
#     for i in citys_select_related:
#         print(i.province)
# 执行的SQL查询：
# SELECT
# 	`app03_city`.`id`,
# 	`app03_city`.`name`,
# 	`app03_city`.`province_id`,
# 	`app03_province`.`id`,
# 	`app03_province`.`name`
# FROM
# 	`app03_city`
# INNER JOIN `app03_province` ON (
# 	`app03_city`.`province_id` = `app03_province`.`id`
# )
#     就只有一次SQL查询，显然大大减少了SQL查询的次数

    # obj = Person.objects.select_related().get()
    # print(obj.living.province)

    # obj = Person.objects.get(firstname=u"张", lastname=u"三").select_related('hometown__name')
    # obj1 = Person.objects.get(firstname=u"张", lastname=u"三").living.province.name
    # obj2 = Person.objects.get(firstname=u"张", lastname=u"三").hometown.name
    # print(obj1, obj2)

    obj3 = Person.objects.select_related('living__province', 'hometown__province').get(firstname=u"张", lastname=u"三")   # 在1.7以前你只能这样做
    print(obj3.living.province.name)
    print(obj3.hometown.province.name)

    # obj4 = Person.objects.select_related('living__province').select_related('hometown__province').get(firstname=u"张", lastname=u"三")
    # print(obj4.living.province.name)
    # print(obj4.hometown.province.name)
    """

    # hb = Province.objects.get(name=u"湖北省")
    # people = []
    # for city in hb.city_set.all():
    #     people.extend(city.birth.all())



    return HttpResponse('ooo')
