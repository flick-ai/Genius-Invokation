from card.action.base import *
from game.game import GeniusGame
from card.character.base import Damage

class RavenBow(WeaponCard):
    '''鸦羽弓'''
    id: int = 0
    name: str = 'Raven Bow'
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    @staticmethod
    def effect(game: GeniusGame, damage: Damage) -> None:
        damage.main_damage += 1

    @staticmethod
    def on_played(game: GeniusGame, target) -> None:
        pass