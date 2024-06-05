from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class TomeoftheEternalFlowWeapon(Weapon):
    name: str = "Tome of the Eternal Flow"
    name_ch =  "万世流涌大典"
    min_add = 0
    max_usage = 1
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.damage_add = self.min_add
        self.usage_round = -1
        self.count = 0

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1
                if self.damage_add > 0:
                    game.current_damage.main_damage += self.damage_add
                    self.damage_add = self.min_add

    def after_damage(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_damage.damage_to == self.from_character:
                self.count += 1
                if self.count == self.max_count:
                    self.damage_add += 2
                    self.count = 0
                    self.usage_round = game.round

    def after_heal(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_heal.heal_to_character == self.from_character:
                self.count += 1
                if self.count == self.max_count:
                    self.damage_add += 2
                    self.count = 0
                    self.usage_round = game.round

    def on_end(self, game: 'GeniusGame'):
        self.damage_add = self.min_add
        self.count = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.after_heal),
        ]



class TomeoftheEternalFlow(WeaponCard):
    id: int = 311108
    name: str = "Tome of the Eternal Flow"
    name_ch = "万世流涌大典"
    weapon_type: WeaponType = WeaponType.CATALYST
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = TomeoftheEternalFlowWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

