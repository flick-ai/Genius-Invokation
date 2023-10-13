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

from game.zone import DiceZone