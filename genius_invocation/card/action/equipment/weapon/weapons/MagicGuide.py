from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class MagicGuideWeapon(Weapon):
    name: str = "Magic Guide"
    name_ch = "魔导绪论"
    max_usage = 1
    id = 31110181
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = self.max_usage
        self.round = -1

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
        ]


class MagicGuide(WeaponCard):
    id: int = 311101
    name: str = "Magic Guide"
    name_ch = "魔导绪论"
    weapon_type: WeaponType = WeaponType.CATALYST
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = MagicGuideWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
