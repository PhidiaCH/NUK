# -*- coding: utf-8 -*-
# dict 運算：keys / values / items / del / 新增
# 知識點 id: c_dict_ops  |  講義程式

fastfood = {'Cheeseburger': 50, 'fries': 25, 'Coke': 35, 'coffee': 45}
items, prices = fastfood.keys(), fastfood.values()
print(items, prices, sum(prices))
print(sorted(items), sorted(prices))
del fastfood['coffee']                 # 刪除
print(list(items))                     # view 會跟著變
print(items & {'Hamburger', 'OJ', 'Coke'})   # {'Coke'}
print(items | {'Hamburger', 'OJ', 'Coke'})
fastfood['coffee'] = 25                # 新增
print('coffee' in fastfood, 'OJ' in fastfood)
for k, v in fastfood.items():          # (key, value) tuple
    print('{0} : {1}'.format(k, v))
