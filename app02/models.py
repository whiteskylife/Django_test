from django.db import models

# Create your models here.


class Business(models.Model):

    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32, default="sa")  # null=True 设置默认为空;default设置默认值为sa


class Host(models.Model):
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32, db_index=True)
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True)
    port = models.IntegerField()
    b = models.ForeignKey(to="Business", to_field="id", on_delete=models.PROTECT)   # 如果省略to_field参数则自动去Business中关联主键


class Application(models.Model):
    """
    Application表只有id和name两个字段
    """
    name = models.CharField(max_length=32)
    r = models.ManyToManyField('Host')          # 创建第三个关系表，表名：app02_application_r

