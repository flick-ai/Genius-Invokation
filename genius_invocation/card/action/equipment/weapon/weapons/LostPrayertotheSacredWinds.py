from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class LostPrayertotheSacredWindsWeapon(Weapon):
    name: str = "Lost Prayer to the Sacred Winds"
    name_ch =  "四风原典"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.bonus_DMG = 0

    def on_damage_add(self, game: 'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element is not ElementType.PIERCING:
                game.current_damage.main_damage += self.bonus_DMG

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.bonus_DMG += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_damage_add),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)
        ]



class LostPrayertotheSacredWinds(WeaponCard):
    id: int = 311106
    name: str = "Lost Prayer to the Sacred Winds"
    name_ch = "四风原典"
    time = 4.3
    weapon_type: WeaponType = WeaponType.CATALYST
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = LostPrayertotheSacredWindsWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

