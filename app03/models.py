from django.db import models

# Create your models here.


class Publish(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    pub_date = models.DateField()
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
    # publish1 = models.ForeignKey(Publish, on_delete=models.CASCADE) # Publish不加引号，Publish要放在Book类上面
    authors = models.ManyToManyField('Author')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(default=20)

    def __str__(self):
        return self.name
