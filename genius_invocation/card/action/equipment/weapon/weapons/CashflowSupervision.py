from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class CashflowSupervisionWeapon(Weapon):
    name: str = "Cashflow Supervision"
    name_ch = "金流监督"
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = 0
        self.count = 0

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    if self.usage > 0:
                        game.current_damage.main_damage += 1
                        self.usage -= 1

    def after_damage(self, game:'GeniusGame'):
        if self.usage == 0:
            if game.current_damage.damage_to == self.from_character:
                self.usage += 1

    def after_heal(self, game:'GeniusGame'):
        if self.usage == 0 and self.count < self.max_count:
            if game.current_heal.heal_to_character == self.from_character:
                self.usage += 1

    def on_end(self, game: 'GeniusGame'):
        self.usage = 0
        self.count = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.after_heal),
        ]



class CashflowSupervision(WeaponCard):
    id: int = 311109
    name: str = "Cashflow Supervision"
    name_ch = "金流监督"
    weapon_type: WeaponType = WeaponType.CATALYST
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = CashflowSupervisionWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

