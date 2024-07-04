from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class PrimordialJadeWingedSpearWeapon(Weapon):
    name: str = "Primordial Jade Winged Spear"
    name_ch = "和璞鸢"
    min_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.round = -1
        self.usage = self.min_usage

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += self.usage

    def on_after_skill(self, game: 'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.min_usage
        if game.current_skill.from_character == self.from_character:
            self.usage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
        ]


class PrimordialJadeWingedSpear(WeaponCard):
    id: int = 311407
    name: str = "Primordial Jade Winged Spear"
    name_ch = "和璞鸢"
    time = 4.3
    weapon_type: WeaponType = WeaponType.POLEARM
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = PrimordialJadeWingedSpearWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
