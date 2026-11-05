# -*- coding: utf-8 -*-
# 變數與指定運算子 =
# 知識點 id: c_variable  |  講義程式

interest_rate = 0.06
capital = 1000000
growth = (1 + interest_rate) ** 32   # Notebook 中可寫成 _ ** 32
print(growth)                        # 6.4533866818853385
print(capital * growth)              # 6453386.681885338
