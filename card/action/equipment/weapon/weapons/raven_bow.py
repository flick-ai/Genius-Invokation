from utils import *
from ..base import WeaponCard
from game.game import GeniusGame


# weapons
class RavenBow(WeaponCard):
    '''鸦羽弓'''
    id: int = 0
    name: str = 'Raven Bow'
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
    
    def effect(self, game: GeniusGame) -> None:
        ##### TODO:
        pass
    