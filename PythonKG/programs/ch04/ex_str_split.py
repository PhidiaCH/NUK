# -*- coding: utf-8 -*-
# Example 4.4 split() / splitlines() 斷字
# 知識點 id: ex_str_split  |  講義程式

string = """Towers of gold are still too little
These hands could hold the world but it'll
Never be enough
Never be enough
For me"""
print(string.lower())
print(string.split(sep=' '))      # 換行字元會黏在單字上
print(string.split(sep='\n'))
string_lines = string.splitlines()
string1 = []
for line in string_lines:
    string1.append(line.split(sep=' '))
print(string1)
