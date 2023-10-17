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

from utils import DiceType
print(DiceType(0) in DiceType)
