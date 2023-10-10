from card.action.base import *
from game.game import GeniusGame
from card.character.base import Damage
from collections import defaultdict

class RavenBow(WeaponCard):
    '''鸦羽弓'''
    id: int = 0
    name: str = 'Raven Bow'
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        # self.usages = defaultdict(int)

    def effect(self, game: GeniusGame, damage: Damage) -> None:
        damage.main_damage += 1

    # def on_played(self, game: GeniusGame, target: int) -> None:
    #     game.players[game.active_player].active_zone.character_list[target].weapon_card = RavenBow