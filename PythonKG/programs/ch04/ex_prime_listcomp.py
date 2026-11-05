# -*- coding: utf-8 -*-
# Example 4.2-8 以 List Comprehension 找質數
# 知識點 id: ex_prime_listcomp  |  講義程式

composite_numbers = [j for i in range(2, 11) for j in range(i*2, 100, i)]
prime_numbers = [x for x in range(2, 100) if x not in composite_numbers]
print('Prime Numbers (< 100) : ', prime_numbers)

# 再精簡成一個運算式
prime_numbers = [x for x in range(2, 100)
                 if x not in [j for i in range(2, 11)
                              for j in range(i*2, 100, i)]]
print(prime_numbers)
