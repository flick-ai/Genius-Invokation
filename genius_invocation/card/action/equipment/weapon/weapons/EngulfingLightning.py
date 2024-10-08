from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class EngulfingLightningWeapon(Weapon):
    name: str = "Engulfing Lightning"
    name_ch = "薙草之稻光"
    id = 31140581
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = self.max_usage
        self.round = -1
        if self.from_character.power == 0:
            self.from_character.get_power(power=1)
            self.usage -= 1

    def on_before(self, game: 'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if self.usage > 0:
            if self.from_character.power == 0:
                self.from_character.get_power(power=1)
                self.usage -= 1

    def on_after(self, game:'GeniusGame'):
        if self.usage > 0:
            if self.from_character.power == 0:
                self.from_character.get_power(power=1)
                self.usage -= 1

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.BEFORE_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.on_before),
            (EventType.AFTER_ANY_ACTION, ZoneType.CHARACTER_ZONE, self.on_after)
        ]


class EngulfingLightning(WeaponCard):
    id: int = 311405
    name: str = "Engulfing Lightning"
    name_ch = "薙草之稻光"
    time = 3.7
    weapon_type: WeaponType = WeaponType.POLEARM
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = EngulfingLightningWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
