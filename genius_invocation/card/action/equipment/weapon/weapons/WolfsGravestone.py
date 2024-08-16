from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class WolfsGravestoneWeapon(Weapon):
    name: str = "Wolf's Gravestone"
    name_ch = "狼的末路"
    id = 31130381
    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                damage_add = 1
                if game.current_damage.damage_to.health_point <= 6:
                    damage_add += 2
                game.current_damage.main_damage += damage_add

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]


class WolfsGravestone(WeaponCard):
    id: int = 311303
    name: str = "Wolf's Gravestone"
    name_ch = "狼的末路"
    weapon_type: WeaponType = WeaponType.CLAYMORE
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = WolfsGravestoneWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
