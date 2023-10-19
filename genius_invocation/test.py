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

from genius_invocation.utils import *
# print(DiceType(0) in DiceType)

# dice = [7,5,5,0,1,2,3,4]
# sort_map = {i:DICENUM-i for i in range(DICENUM)}
# print(sort_map)
# so = sorted(dice, key=lambda x:sort_map[x], reverse=True)
# print(so)
# idx = sorted(range(len(dice)), key=lambda x:sort_map[dice[x]], reverse=True)
# print(idx)
# so = [7]
# dice = [7,7,1]
# print(dice.count(7))

from rich import print
from rich.layout import Layout

layout = Layout()

layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)

layout["lower"].split_row(
    Layout(name="support"),
    Layout(name="character"),
    Layout(name="summon"),
    Layout(name="dice")
)

layout["lower"]['summon'].size = None
layout["lower"]['summon'].ratio = 2

layout["lower"]['character'].size = None
layout["lower"]['character'].ratio = 5

layout["lower"]['support'].size = None
layout["lower"]['support'].ratio = 2

layout["lower"]['dice'].size = None
layout["lower"]['dice'].ratio = 1

layout["lower"]['dice']

print(layout)