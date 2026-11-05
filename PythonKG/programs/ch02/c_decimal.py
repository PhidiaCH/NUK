# -*- coding: utf-8 -*-
# Decimal 十進位精確運算
# 知識點 id: c_decimal  |  講義程式

from decimal import Decimal
print((-15) % 4)                    # 1
print((-15) // 4)                   # -4
print(Decimal(-15) % Decimal(4))    # -3
print(Decimal(-15) // Decimal(4))   # -3
