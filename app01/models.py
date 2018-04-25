from django.db import models

# Create your models here.


# class UserInfo(models.Model):
#
#     username = models.CharField(max_length=32)
#     password = models.CharField(max_length=64)


class Person(models.Model):
    name = models.CharField(max_length=50)


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)


class Department(models.Model):
    '''''
    some other filed
    '''
    super_department = models.ForeignKey('self', on_delete=models.CASCADE)
