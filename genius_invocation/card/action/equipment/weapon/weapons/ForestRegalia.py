from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon, Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class ForestRegaliaStatus(Status):
    name: str = "Forest Regalia"
    name_ch = "森林王器"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None):
        super().__init__(game, from_player, from_character)

    def on_after_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                element_dice = ElementToDice[get_my_active_character(game).element]
                self.from_player.dice_zone.add([element_dice.value for _ in range(2)])
                self.on_destroy(game)

    def on_end(self, game: 'GeniusGame'):
        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end)
        ]


class ForestRegaliaWeapon(Weapon):
    name: str = "Forest Regalia"
    name_ch = "森林王器"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        entity = self.from_character.character_zone.has_entity(ForestRegaliaStatus)
        if entity is None:
            entity = ForestRegaliaStatus(game, from_player, from_character)
            self.from_character.character_zone.add_entity(entity)

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
        ]


class ForestRegalia(WeaponCard):
    id: int = 311307
    name: str = "Forest Regalia"
    name_ch = "森林王器"
    weapon_type: WeaponType = WeaponType.CLAYMORE
    cost_num: int = 3
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = ForestRegaliaWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
