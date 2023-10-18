import numpy as np
from typing import TYPE_CHECKING
# a = [1,2,3,4,5]
# # np.random.shuffle(a)
# a.insert(5,6)
# print(a)

# a = []

# class A:
#     def __init__(self):
#         self.a = []
#         self.b = 2

#     def aaa(self):
#         self.a.append(A())

# alist = A()
# alist.aaa()
# print(alist.a[0].aaa)
# if TYPE_CHECKING:
#     from test2 import B


# # def testf(a: 'B'):
# #     print(a.a)

# # testf(1.44)
class person:
    def __init__(self) -> None:
        pass

class me(person):
    def __init__(self) -> None:
        super().__init__()

I = me()
# print(type(I), type(I)==me, type(I)==person)
# print(isinstance(I, 'me'), isinstance(I, person))
# print(-1%3)

from utils import *
# print(DiceType(0) in DiceType)

# dice = [7,5,5,0,1,2,3,4]
# sort_map = {i:DICENUM-i for i in range(DICENUM)}
# print(sort_map)
# so = sorted(dice, key=lambda x:sort_map[x], reverse=True)
# print(so)
# idx = sorted(range(len(dice)), key=lambda x:sort_map[dice[x]], reverse=True)
# print(idx)
so = [7]
dice = [7,7,1]
print(dice.count(7))