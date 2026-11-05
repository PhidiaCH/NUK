# -*- coding: utf-8 -*-
# enumerate()
# 知識點 id: f_enumerate  |  講義程式

languages = ['Python', 'R', 'Scala']
print(list(enumerate(languages)))           # [(0, 'Python'), ...]
print(list(enumerate(languages, start=1)))
for index, element in enumerate(languages, start=1):
    print(index, element)
