# -*- coding: utf-8 -*-
# 4.4 str 字串方法
# 知識點 id: c_str_methods  |  講義程式

s = '  Hello Python  '
print(s.strip(), '|', s.upper(), '|', s.lower())
print('python'.capitalize(), 'Python'.center(12, '*'))
print('banana'.count('a'), 'banana'.find('n'), 'banana'.replace('a', 'A'))
print('-'.join(['2024', '03', '01']))
print('a,b,,c'.split(','))
print('{0} is {1} years old'.format('Alice', 20))
print('Ünïcode'.encode('utf-8'))
