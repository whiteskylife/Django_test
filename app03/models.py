from django.db import models

# Create your models here.


class UserInf(models.Model):

    user = models.CharField(max_length=32)


class UserType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class User(models.Model):

    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)
    ut = models.ForeignKey(to='UserType', to_field='id', on_delete=models.PROTECT)

    t = models.ManyToManyField('self')
