# -*- coding=utf-8 -*-
# def fact(n):
#     print(n)
#     if n==1:
#         return 1
#     return n * fact(n - 1)
# fact(10)


def num(a, b):
    a += 1
    b -= 1
    print("a+b: {}.{}".format(a, b))
    if b is 0:
        return a, b
    return num(a, b)
print(num(1, 1000))