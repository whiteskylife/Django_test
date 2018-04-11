# !/usr/bin/env python
# -*-coding:utf-8 -*-

#
# class Foo:
#     def __repr__(self):
#         return 'in Foo````````````````````'
#
#     def m1(self):
#         print('this is Foo 1')
#
#
# class Foo2(Foo):
#
#     def m1(self):
#         # print('this is Foo2-----------')
#         pass
#
#
# obj = Foo2()
# obj.m1()
# print(obj)
#

v = [lambda x: i*x for i in range(10)]

for func in v:
    print(func(2))