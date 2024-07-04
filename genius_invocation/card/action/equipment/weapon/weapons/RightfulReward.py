from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class RightfulRewardWeapon(Weapon):
    name: str = "Rightful Reward"
    name_ch = "公义的酬报"
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.principleofjustice = 0

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.damage_type == SkillType.ELEMENTAL_BURST:
                if game.current_damage.main_damage_element is not ElementType.PIERCING:
                    game.current_damage.main_damage += 2

    def after_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to == get_active_character(game, self.from_player.index):
            self.principleofjustice += 1
            if self.principleofjustice == self.max_count:
                self.principleofjustice = 0
                self.from_character.get_power(power=1)


    def after_heal(self, game:'GeniusGame'):
        if game.current_heal.heal_to_character == get_active_character(game, self.from_player.index):
            self.principleofjustice += 1
            if self.principleofjustice == self.max_count:
                self.principleofjustice = 0
                self.from_character.get_power(power=1)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
        ]


class RightfulReward(WeaponCard):
    id: int = 311408
    name: str = "Rightful Reward"
    name_ch = "公义的酬报"
    time = 4.6
    weapon_type: WeaponType = WeaponType.POLEARM
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = RightfulRewardWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
