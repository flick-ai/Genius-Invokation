from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class TulaytullahsRemembrance(WeaponCard):
    name = "Tulaytullah's Remembrance"
    name_ch =  "图莱杜拉的回忆"
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = self.max_usage

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def on_calculate_dice(self, game:'GeniusGame'):
        if self.from_player.dice_zone.num()%2 != 0:
            return False
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                if game.current_dice.from_character == self.from_character:
                    if self.usage > 0:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_skill(self, game:"GeniusGame"):
        if self.on_calculate_dice(game):
            self.usage -= 1

    def on_end(self, game: 'GeniusGame'):
        self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice)
        ]



class TulaytullahsRemembrance(WeaponCard):
    id: int = 311107
    name: str = "Tulaytullah's Remembrance"
    name_ch = "图莱杜拉的回忆"
    time = 4.3
    weapon_type: WeaponType = WeaponType.CATALYST
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = TulaytullahsRemembrance

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

