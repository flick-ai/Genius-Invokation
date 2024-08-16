from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class SplendorofTranquilWatersWeapon(Weapon):
    name: str = "Splendor of Tranquil Waters"
    name_ch = "静水流涌之辉"
    max_usage = 12
    max_count = 1
    id = 31150881
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.count = 0
        self.lakelight = 0 
        self.is_use = False
    
    def on_calculate_dice(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.from_character == self.from_character:
                if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                    if self.lakelight >= self.max_usage and self.count < self.max_count:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] = max(0, game.current_dice.cost[1]['cost_num'] - 2)
                            return True
        return False

    def on_skill(self, game: 'GeniusGame'):
        if self.on_calculate_dice(game):
            self.lakelight -= self.max_usage
            self.count += 1
            self.is_use = True
    
    def after_skill(self, game: 'GeniusGame'):
        if self.is_use:
            self.is_use = False

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                if game.current_damage.damage_type == SkillType.NORMAL_ATTACK:
                    if self.is_use:
                        game.current_damage.main_damage += 1
                        self.is_use = False

    def after_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player == self.from_player:
            self.lakelight += 1

    def after_heal(self, game:'GeniusGame'):
        if game.current_heal.heal_to_character.from_player == self.from_player:
            self.lakelight += 1

    def on_end(self, game: 'GeniusGame'):
        self.count = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.after_heal),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate_dice),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill)
        ]


class SplendorofTranquilWaters(WeaponCard):
    id: int = 311508
    name: str = "Splendor of Tranquil Waters"
    name_ch = "静水流涌之辉"
    time = 4.7
    weapon_type: WeaponType = WeaponType.SWORD
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = SplendorofTranquilWatersWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
