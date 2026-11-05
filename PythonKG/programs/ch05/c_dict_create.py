# -*- coding: utf-8 -*-
# dict 的 5 種產生方式
# 知識點 id: c_dict_create  |  講義程式

gpa0 = {'C': 2.0, 'B': 3.0, 'A': 4.0, 'F': 'Fail'}
gpa1 = dict(A=4.0, B=3.0, C=2.0, F='Fail')
gpa2 = dict({'B': 3.0, 'A': 4.0, 'F': 'Fail', 'C': 2.0})
gpa3 = dict([('F', 'Fail'), ('C', 2.0), ('A', 4.0), ('B', 3.0)])
gpa4 = dict(zip(['F', 'C', 'B', 'A'], ['Fail', 2.0, 3.0, 4.0]))
print(gpa0 == gpa1 == gpa2 == gpa3 == gpa4)   # True
