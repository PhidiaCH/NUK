# -*- coding: utf-8 -*-
# 練習：以 dict comprehension 精簡 log 表
# 知識點 id: q5_log  |  參考解答 (非講義原文)

from math import log
log_x = {x: round(log(x, 10), 4) for x in (1, 2, 3, 5, 10, 50, 100)}
print(log_x)
