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


class Boy_Boy_Boy(models.Model):
    name = models.CharField(max_length=32)


class Girl_Girl_Girl(models.Model):
    name = models.CharField(max_length=32)
    m = models.ManyToManyField('Boy_Boy_Boy', through='Love_Love_Love', through_fields=('g', 'b'))  # 只让其生成3张表，如果不加后面产生生成4张表


class Love_Love_Love(models.Model):
    b = models.ForeignKey('Boy_Boy_Boy', on_delete=models.PROTECT)
    g = models.ForeignKey('Girl_Girl_Girl', on_delete=models.PROTECT)
