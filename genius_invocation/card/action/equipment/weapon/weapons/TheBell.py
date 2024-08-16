from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon, Combat_Shield

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class TheBellWeapon(Weapon):
    '''钟剑'''
    id = 31130581
    name = "The Bell"
    name_ch = "钟剑"
    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1
    
    def after_use_skill(self, game: 'GeniusGame'):
        if self.current_round == game.round: return
        combat_shield = self.from_character.from_player.team_combat_status.has_shield(Shield_of_Bell)
        if combat_shield:
            combat_shield.update()
        else:
            combat_shield = Shield_of_Bell(game, self.from_character.from_player, self.from_character)
            self.from_character.from_player.team_combat_status.add_entity(combat_shield)

    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: "Character"= None, weapon_card: 'WeaponCard' = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.current_round = -1

    def update(self):
        self.current_round = -1
        
    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_use_skill)
        ]

class Shield_of_Bell(Combat_Shield):
    id = 31130551
    name = "Shield of Bell"
    name_ch = "钟剑之盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.current_usage = 1
        self.max_usage = 2

    def update(self):
        if self.current_usage < self.max_usage:
            self.current_usage += 1

class TheBell(WeaponCard):
    '''钟剑'''
    id = 311305
    name = "The Bell"
    name_ch = "钟剑"
    time = 3.7
    weapon_type = WeaponType.CLAYMORE
    cost_num = 3
    cost_type = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = TheBellWeapon
    