from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon, Shield, Combat_Shield

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.entity.character import Character


class VortexVanquisherWeapon(Weapon):
    name: str = "Vortex Vanquisher"
    name_ch = "贯虹之槊"
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character: 'Character'= None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = self.max_usage
        self.round = -1

    def on_after_skill(self, game: 'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if self.usage > 0:
            if game.current_skill.from_character == self.from_character:
                if game.current_skill.type == SkillType.ELEMENTAL_SKILL:
                    combat_shield = self.from_player.team_combat_status.has_shield(Combat_Shield)
                    if combat_shield is not None:
                        combat_shield.current_usage += 1
                        self.usage -= 1


    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                damage_add = 1
                if self.from_player.team_combat_status.shield is not [] or self.from_character.character_zone.has_entity(Shield):
                    damage_add += 1
                game.current_damage.main_damage += damage_add

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add)
        ]



class VortexVanquisher(WeaponCard):
    id: int = 311404
    name: str = "Vortex Vanquisher"
    name_ch = "贯虹之槊"
    weapon_type: WeaponType = WeaponType.POLEARM
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = VortexVanquisherWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
