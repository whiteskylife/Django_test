#!/usr/bin/env python
# -*-coding:utf-8 -*-


class Foo:
    def __repr__(self):
        return 'in Foo````````````````````'

    def m1(self):
        print('this is Foo 1')


class Foo2(Foo):

    def m1(self):
        print('this is Foo2-----------')


obj = Foo2()
obj.m1()
print(obj)


