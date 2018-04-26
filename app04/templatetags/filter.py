from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def filter_all(arg_dict, k):
    '''
    逻辑：对两种类型的索引显示"全部"时添加高亮
    {% if arg_dict.article_type_id == 0 %}
        <a class="active" href="/article-0-{{ arg_dict.category_id }}">全部</a>
    {% else %}
        <a href="/article-0-{{ arg_dict.category_id }}">全部</a>
    {% endif %}
    :param arg_dict: 视图函数中的kwarg字典，如：{'category_id': '2', 'article_type_id': '1'}
    :param k: 前端组合索引的两种分类：1.article_type_id  2.category_id
    :return:  返回a标签
    '''
    ret = ''
    if k == 'article_type_id':
        if arg_dict['article_type_id'] == 0:
            ret = '<a class="active" href="/article-0-%s">全部</a>' % arg_dict['category_id']
        else:
            ret = '<a href="/article-0-%s">全部</a>' % arg_dict['category_id']
    elif k == 'category_id':
        if arg_dict['category_id'] == 0:
            ret = '<a class="active" href="/article-%s-0">全部</a>' % arg_dict['article_type_id']
        else:
            ret = '<a href="/article-%s-0">全部</a>' % arg_dict['article_type_id']
    return mark_safe(ret)


@register.simple_tag
def filter_article_type(arg_dict, g, h):
    """
        逻辑：
        {% for row in article_type_list %}
        {% if row.id == arg_dict.article_type_id %}
            <a class="active" href="/article-{{ row.id }}-{{ arg_dict.category_id }}">{{ row.caption }}</a>
        {% else %}
            <a href="/article-{{ row.id }}-{{ arg_dict.category_id }}">{{ row.caption }}</a>
        {% endif %}
    {% endfor %}
    :param arg_dict:
    :param g: article_type_list、category_list这两个列表，用于循环生成标签
    :param h: article_type_list、category_list这两个列表的字符串形式传参，流程控制
    :return:很多a标签
    """
    a = []
    for row in g:
        if h == 'article_type_list':
            if row[0] == arg_dict['article_type_id']:
                s = '<a class="active" href="/article-%s-%s">%s</a>' % (row[0], arg_dict['category_id'], row[1])
            else:
                s = '<a href="/article-%s-%s">%s</a>' % (row[0], arg_dict['category_id'], row[1])
            a.append(s)
        elif h == 'category_list':
            if row.id == arg_dict['category_id']:
                s = '<a class="active" href="/article-%s-%s">%s</a>' % (row.id, arg_dict['article_type_id'], row.caption)
            else:
                s = '<a href="/article-%s-%s">%s</a>' % (arg_dict['article_type_id'], row.id, row.caption)
            a.append(s)
    ret = ''.join(a)
    return mark_safe(ret)
