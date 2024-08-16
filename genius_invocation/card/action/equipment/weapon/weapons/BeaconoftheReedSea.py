from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class BeaconoftheReedSeaWeapon(Weapon):
    name: str = "Beacon of the Reed Sea"
    name_ch = "苇海信标"
    id = 31130681
    max_usage = 1
    max_count = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.round_damage = -1
        self.round_skill = -1

        self.usage_damage = self.max_usage
        self.usage_skill = self.max_usage

        self.add_damage = 0
        self.add_skill = 0

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1
                if self.add_damage > 0:
                    game.current_damage.main_damage += self.add_damage
                if self.add_skill > 0:
                    game.current_damage.main_damage += self.add_skill

    def on_after_skill(self, game: 'GeniusGame'):
        if self.round_skill != game.round:
            self.round_skill = game.round
            self.usage_skill = self.max_usage
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.ELEMENTAL_SKILL:
                if self.usage_skill > 0:
                    self.add_skill = self.max_count
                    self.usage -= 1

    def after_damage(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            self.round_damage = game.round
            self.usage_damage = self.max_usage
        if game.current_damage.damage_to == self.from_character:
            if self.usage_damage > 0:
                self.add_damage = self.max_count
                self.usage_damage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.after_damage),
        ]


class BeaconoftheReedSea(WeaponCard):
    id: int = 311306
    name: str = "Beacon of the Reed Sea"
    name_ch = "苇海信标"
    time = 4.3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = BeaconoftheReedSeaWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
