# -*- coding: utf-8 -*-
# tuple() 建構子
# 知識點 id: f_tuple  |  講義程式

print(tuple())                    # ()
print(tuple(range(2, 7)))         # (2, 3, 4, 5, 6)
print(tuple('abc'))               # ('a', 'b', 'c')
print(tuple(['a', 'b', 'c']))
t1 = (('ABC', 'NBC', 'CBS'), ('Python', 123, 3.1416), (2.71828, 1.732))
print(tuple(t1[1:2]))             # (('Python', 123, 3.1416),)
print(tuple(t1[1]))               # ('Python', 123, 3.1416)
# tuple('a', 'b', 'c')  # TypeError: tuple expected at most 1 argument
