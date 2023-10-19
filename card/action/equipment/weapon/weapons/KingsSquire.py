from utils import *
from ..base import WeaponCard
from typing import TYPE_CHECKING
from entity.status import Weapon, Status

if TYPE_CHECKING:
    from game.game import GeniusGame


class StatusOfKingsSquire(Status):
    
    def on_calculate(self, game: 'GeniusGame'):
        if game.current_damage.damage_from is self.from_player.character:
            game.current_damage.main_damage += 1

        
    def on_end_phase(self, game: 'GeniusGame'):
        '''
        仅本回合生效
        '''
        if game.active_player == self.from_player:
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase)
        ]



# weapons
class RavenBowWeapon(Weapon):
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
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
        idx = game.current_action.target_idx
        target_character = game.active_player.character_list[idx]
        status = StatusOfKingsSquire(game, game.active_player, target_character)
        target_character.character_zone.add_entity(status)

