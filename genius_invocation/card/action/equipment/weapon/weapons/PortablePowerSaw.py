from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class PortablePowerSawWeapon(Weapon):
    id: int = 31130981
    name: str = "Portable Power Saw"
    name_ch = "便携动力锯"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.round_usage = 1
        self.stoicssymbol = 0
        self.add_damage = False

    def on_damage_execute(self, game: 'GeniusGame'):
        if self.round_usage <=0 :
            return
        if game.current_damage.damage_to == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PIERCING:
                return
            if game.current_damage.main_damage > 0:
                max_id = max_count_card()
                if max_id == None:
                    return
                else:
                    game.current_damage.main_damage -= 1
                self.stoicssymbol += 1
                self.round_usage -= 1

    def on_add_damage(self, game:'GeniusGame'):
        if self.add_damage:
            game.current_damage.main_damage += 1
            self.add_damage = False

    def after_use_skill(self, game: 'GeniusGame'):
        if self.add_damage:
            self.add_damage = False

    def on_use_skill(self, game: 'GeniusGame'):
        if game.current_skill.from_character == self.from_character:
            if self.stoicssymbol > 0:
                self.add_damage = True
                self.from_player.get_card(num=self.stoicssymbol)
                self.stoicssymbol = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_damage_execute),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_use_skill),
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_use_skill)
        ]


class PortablePowerSaw(WeaponCard):
    id: int = 311309
    name: str = "Portable Power Saw"
    name_ch = "便携动力锯"
    time = 5.1
    weapon_type: WeaponType = WeaponType.CLAYMORE
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = PortablePowerSawWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)