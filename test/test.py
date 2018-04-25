# !/usr/bin/env python
# -*-coding:utf-8 -*-

# class Foo:
#     test = 'asd'
#
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
#
# print(obj.test)
#
#
# v = [lambda x: i*x for i in range(10)]
#
# for func in v:
#     print(func(2))
'''
a = [1, 2, 3]
a_l = a.__iter__()
# print(a_l.__next__())
# print(a_l.__next__())
# print(a_l.__next__())

while True:
    try:
        print(a_l.__next__())
    except StopIteration:
        break
'''


# 生成器表达式
# goods_list3 = (i for i in range(10))     # 生成器对象转列表：goods_list3 = list((i for i in range(10)))
#
# print(goods_list3.)
#

# def lay_eggs(num):
#     for egg in range(num):
#         res = '蛋%s' % egg
#         yield res
#         print('下完一个蛋')
#
#
# laomuji = lay_eggs(10)  # 我们拿到的是一只母鸡
# print(laomuji)
# print(laomuji.__next__())
# print(laomuji.__next__())
# print(laomuji.__next__())
# egg_l = list(laomuji)
# print(egg_l)


# chicken = ('鸡蛋%s' % i for i in range(10))
#
# print(chicken.__next__())
# print(chicken.__next__())
# print(chicken.__next__())


# 总结：
# 1.把列表解析的[]换成()得到的就是生成器表达式
# 2.列表解析与生成器表达式都是一种便利的编程方式，只不过生成器表达式更节省内存
# 3.Python不但使用迭代器协议，让for循环变得更加通用。大部分内置函数，也是使用迭代器协议访问对象的。例如， sum函数是Python的内置函数，该函数使用迭代器协议访问对象，而生成器实现了迭代器协议，所以，我们可以直接这样计算一系列值的和：

# sum(x ** 2 for x in xrange(4))
# 而不用多此一举的先构造一个列表：sum([x ** 2 for x in xrange(4)])

#
# def index_words(text):
#     result = []
#     if text:
#         result.append(0)
#     for index, letter in enumerate(text, 1):
#         if letter == 'a':
#             result.append(index)
#     return result
#
#
# print(index_words('hello alex da sb'))
#
#
# def index_words(text):
#     if text:
#         yield 0
#     for index, letter in enumerate(text, 1):
#         if letter == 'a':
#             yield index
#
#
# g = index_words('hello alex da sb')
# print(g)
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())
# print(g.__next__())  # 报错


# def add(n, i):
#     print('n:', n, 'i:', i, 'n+i:', n + i)
#     return n + i
#
#
# f = [0, 1]
#
# for n in [1, 2]:
#     print(n, 1)
#     g = (add(n, i) for i in f)
#     print(n, 2)
#     print(list(g))

# ----------------interview
def extend_list(val, list=[]):
    print(id(list), '---------------------')
    list.append(val)
    print(id(list), '---------------------')
    return list


list1 = extend_list(10)
print('list1 *****', id(list1), list1)
list2 = extend_list(123)
print('list2 *****', id(list2))
list3 = extend_list('a', [666])
print(list1)
print(list2)
print(list3)


# class Parent(object):
#     x = 1
#
#
# class Child1(Parent):
#     pass
#
#
# class Child2(Parent):
#     pass
#
#
# print(Parent.x, Child1.x, Child2.x)
# Child1.x = 2
# print(Parent.x, Child1.x, Child2.x)
# Parent.x = 3
# print(Parent.x, Child1.x, Child2.x)
