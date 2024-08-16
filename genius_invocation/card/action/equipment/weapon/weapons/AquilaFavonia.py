from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class AquilaFavoniaWeapon(Weapon):
    name: str = "Aquila Favonia"
    name_ch = "风鹰剑"
    max_usage = 2
    id = 31150381
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = self.max_usage
        self.round = -1

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def on_after_skill(self, game: 'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if game.current_skill.from_character.from_player != self.from_player and self.from_character.is_active:
            if self.usage > 0:
                self.from_character.heal(heal=1, game=game)
                self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill)
        ]


class AquilaFavonia(WeaponCard):
    id: int = 311503
    name: str = "Aquila Favonia"
    name_ch = "风鹰剑"
    weapon_type: WeaponType = WeaponType.SWORD
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = AquilaFavoniaWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
