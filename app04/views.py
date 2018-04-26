from django.shortcuts import render
from app04 import models
# Create your views here.
import requests

def article(request, **kwargs):
    # article_type_list = models.ArticleType.objects.all()
    article_type_list = models.Article.type_choice      # 通过静态字段形式访问
    category_list = models.Category.objects.all()
    condition = {}
    if not kwargs:                      # 第一次访问时，字典中的值不存在，设置初 值
        kwargs['article_type_id'] = 0
        kwargs['category_id'] = 0
    for k, v in kwargs.items():        # 把值为0的k,v过滤排除掉，字典如：{'category_id': '2', 'article_type_id': '1'}
        kwargs[k] = int(v)          # 把字典中的字符串转换位数字，传给前台
        if v == '0':
            pass
        else:
            condition[k] = v

    result = models.Article.objects.filter(**condition)
    return render(request,
                  'article.html',
                  {
                      'result': result,
                      'article_type_list': article_type_list,
                      'category_list': category_list,
                      'arg_dict': kwargs,
                  }
                  )


