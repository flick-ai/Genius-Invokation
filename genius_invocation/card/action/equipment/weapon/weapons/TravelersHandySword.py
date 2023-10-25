from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class TravelersHandySwordWeapon(Weapon):
    name: str = "Traveler's Handy Sword"
    name_ch = "旅行剑"
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
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


class TravelersHandySword(WeaponCard):
    id: int = 311501
    name: str = "Traveler's Handy Sword"
    name_ch = "旅行剑"
    weapon_type: WeaponType = WeaponType.SWORD
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = TravelersHandySwordWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
