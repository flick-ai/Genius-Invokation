from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


# weapons
class RavenBowWeapon(Weapon):
    id: int = 31120181
    name: str = 'Raven Bow'
    name_ch = '鸦羽弓'
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add)
        ]


class RavenBow(WeaponCard):
    '''鸦羽弓'''
    id: int = 311201
    name: str = 'Raven Bow'
    name_ch = '鸦羽弓'
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = RavenBowWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
