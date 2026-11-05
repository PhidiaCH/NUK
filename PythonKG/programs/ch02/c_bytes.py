# -*- coding: utf-8 -*-
# bytes 位元組常值
# 知識點 id: c_bytes  |  講義程式

bytes_string = b'Hello Python!'
print(bytes_string)                              # b'Hello Python!'
print(str(bytes_string))                         # "b'Hello Python!'"
print(str(bytes_string, encoding='UTF-8'))       # bytes → str
print(bytes('Hi there!', encoding='ASCII'))      # str → bytes
