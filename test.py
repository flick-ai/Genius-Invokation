class person:
    def __init__(self) -> None:
        pass

class me(person):
    def __init__(self) -> None:
        super().__init__()
    
I = me()
# print(type(I), type(I)==me, type(I)==person)
# print(isinstance(I, me), isinstance(I, person))
# print(-1%3)

from enum import Enum
class DiceType(Enum):
    CRYO = 0 # 冰
    HYDRO = 1 # 水
    PYRO = 2 # 火
    ELECTRO = 3 # 雷
    ANEPMO = 4 # 风
    GEO = 5 # 岩
    DENDRO = 6 # 草
    OMNI = 7 # 万能

print(DiceType.CRYO.name)