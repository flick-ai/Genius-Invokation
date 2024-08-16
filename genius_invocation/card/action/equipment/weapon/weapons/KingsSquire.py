from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon, Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class StatusOfSummeru(Status):
    name = "Status Of Summeru's Weapon"
    name_ch = '须弥武器状态'
    id = 31120621
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 1
        
    def on_calculate(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type is SkillType.ELEMENTAL_SKILL:
                if game.current_dice.from_character == self.from_character:
                    if game.current_dice.cost[0]['cost_num']>0:
                        game.current_dice.cost[0]['cost_num'] -= 2
                        game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num'])
                        return True
        return False
    
    def on_skill(self, game: 'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)                        
        
    def on_end_phase(self, game: 'GeniusGame'):
        '''
        仅本回合生效
        '''
        if game.active_player == self.from_player:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill)
        ]



# weapons
class KingsSquire(Weapon):
    name: str = "King's Squire"
    name_ch = "王下近侍"
    id = 31120681
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add)
        ]


class KingsSquire(WeaponCard):
    '''王下近侍'''
    id: int = 311206
    name: str = "King's Squire"
    name_ch = "王下近侍"
    time = 4.0
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE
    
    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = KingsSquire

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
        idx = game.current_action.target_idx
        target_character = game.active_player.character_list[idx]
        if target_character.character_zone.has_entity(StatusOfSummeru) == None:
            status = StatusOfSummeru(game, game.active_player, target_character)
            target_character.character_zone.add_entity(status)

