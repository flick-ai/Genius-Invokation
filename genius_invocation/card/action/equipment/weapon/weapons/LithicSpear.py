from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon, Shield

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class LithicSpearShield(Shield):
    name = "Shield of Lithic Spear"
    name_ch = "千岩之盾"
    id = 31140241
    def __init__(self, usage, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.max_usage = usage
        self.current_usage = usage

    def update(self):
        self.current_usage = self.max_usage

class LithicSpearWeapon(Weapon):
    name: str = "Lithic Spear"
    name_ch = "千岩长枪"
    max_usage = 1
    id = 31140281
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.usage = self.max_usage
        self.round = -1

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add)
        ]


class LithicSpear(WeaponCard):
    id: int = 311402
    name: str = "Lithic Spear"
    name_ch = "千岩长枪"
    weapon_type: WeaponType = WeaponType.POLEARM
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = LithicSpearWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
        shields = 0
        for character in game.active_player.character_list:
            if character.country == CountryType.LIYUE:
                shields += 1
        idx = game.current_action.target_idx
        target_character = game.active_player.character_list[idx]
        has_shield = target_character.character_zone.has_entity(LithicSpearShield)
        if has_shield != None:
            has_shield.update()
        else:
            new_shield = LithicSpearShield(shields, game, game.active_player, target_character)
            target_character.character_zone.add_entity(new_shield)
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.7] = " 调整了「七圣召唤」中，装备牌「千岩长枪」的效果：现在已被击倒的角色也会被计算在内"
        return log
        
        
