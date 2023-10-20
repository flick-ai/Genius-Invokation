from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon, Combat_Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class MillennialMovementFarewellSong(Combat_Status):
    '''
    千年的大乐章·别离之歌
    '''
    usage: int = 2
    max_usage: int = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = self.usage
    
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from is not None:
            if game.current_damage.damage_from.from_player == self.from_player:
                if game.current_damage.main_damage_element is not ElementType.PIERCING:
                    game.current_damage.main_damage += 1

    def update(self):
        self.current_usage = self.usage

    def on_begin_phase(self, game: 'GeniusGame'):
        if game.active_player == self.from_character.from_player:
            self.current_usage -= 1
            if self.current_usage <= 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.ACTIVE_ZONE, self.on_damage_add),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.ACTIVE_ZONE, self.on_begin_phase)
        ]

# weapon
class ElegyForTheEndWeapon(Weapon):
    '''终末嗟叹之诗'''
    id: int = 311205
    name: str = 'Elegy for the End'
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def after_use_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if game.current_skill.type == SkillType.ELEMENTAL_BURST:
                # 生成千年的大乐章·别离之歌
                status = self.from_player.team_combat_status.has_status(MillennialMovementFarewellSong)
                if not status:
                    millennial_movement_farewell_song = MillennialMovementFarewellSong(game, self.from_player, None)
                    self.from_player.team_combat_status.add_entity(millennial_movement_farewell_song)
                else:
                    status.update()
                

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_use_skill)
        ]


class ElegyForTheEnd(WeaponCard):
    '''终末嗟叹之诗'''
    id: int = 311205
    name: str = 'Elegy for the End'
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = ElegyForTheEndWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
