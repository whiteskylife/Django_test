from django.db import models

# Create your models here.

#
# class Publish(models.Model):
#     name = models.CharField(max_length=32)
#     city = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.name
#
#
# class Book(models.Model):
#     name = models.CharField(max_length=20)
#     price = models.IntegerField()
#     pub_date = models.DateField()
#     publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
#     # publish1 = models.ForeignKey(Publish, on_delete=models.CASCADE) # Publish不加引号，Publish要放在Book类上面
#     authors = models.ManyToManyField('Author')
#
#     def __str__(self):
#         return self.name
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=32)
#     age = models.IntegerField(default=20)
#
#     def __str__(self):
#         return self.name
#
# #
# # class Book_Author(models.Model):
# #     book = models.ForeignKey('Book', on_delete=models.CASCADE)
# #     author = models.ForeignKey('Author', on_delete=models.CASCADE)
#
#
# class Province(models.Model):
#     name = models.CharField(max_length=10)
#
#     def __unicode__(self):
#         return self.name
#
#
# class City(models.Model):
#     name = models.CharField(max_length=5)
#     province = models.ForeignKey(Province, on_delete=models.CASCADE)
#
#     def __unicode__(self):
#         return self.name
#
#
# class Person(models.Model):
#     firstname = models.CharField(max_length=10)
#     lastname = models.CharField(max_length=10)
#     visitation = models.ManyToManyField(City, related_name="visitor")
#     hometown = models.ForeignKey(City, related_name="birth", on_delete=models.CASCADE)
#     living = models.ForeignKey(City, related_name="citizen", on_delete=models.CASCADE)
#
#     def __unicode__(self):
#         return self.firstname + self.lastname
#
#
# class Order(models.Model):
#     customer = models.ForeignKey(Person, on_delete=models.CASCADE)
#     orderinfo = models.CharField(max_length=50)
#     time = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return self.orderinfo


class UserType(models.Model):
    caption = models.CharField(max_length=32)


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    user_type = models.ForeignKey(to='UserType', to_field='id', on_delete=models.CASCADE)

