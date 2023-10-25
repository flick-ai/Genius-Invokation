from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class AmosBowWeapon(Weapon):
    name: str = "Amos' Bow"
    name_ch = "阿莫斯之弓"
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage
        self.round = -1

    def on_add_damage(self, game:'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                damage_add = 1
                if self.usage > 0:
                    sum_cost = game.current_skill.energy_cost
                    for cost in game.current_skill.cost:
                        sum_cost += cost['cost_num']
                    if sum_cost >= 5:
                        damage_add += 2
                        self.usage -= 1
                game.current_damage.main_damage += damage_add

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]


class AmosBow(WeaponCard):
    id: int = 311204
    name: str = "Amos' Bow"
    name_ch = "阿莫斯之弓"
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = AmosBowWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
