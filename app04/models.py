from django.db import models

# Create your models here.


class Category(models.Model):
    caption = models.CharField(max_length=16)


# class ArticleType(models.Model):
#     caption = models.CharField(max_length=16)


class Article(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=55)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE)
    # 通过静态字段实现，直接写到内存，不写到表中
    type_choice = (
        (1, 'python'),
        (2, 'openstack'),
        (3, 'linux'),
    )
    article_type_id = models.IntegerField(choices=type_choice)

