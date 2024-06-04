from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class EndoftheLineWeapon(Weapon):
    name: str = "End of the Line"
    name_ch = "竭泽"
    max_catch = 2
    max_count = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.catch = 0
        self.count = 0

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if self.catch > 0:
                game.current_damage.main_damage += self.catch
                self.from_player.get_card(num=self.catch)
                self.catch = 0
    
    def on_play_card(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_card.name not in self.from_player.card_zone.card_name:
                if self.count < self.max_count:
                    self.catch = min(2, self.catch + 1)
                    self.count += 1
    
    def on_end(self, game: 'GeniusGame'):
        self.count = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.AFTER_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play_card),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
        ]


class EndoftheLine(WeaponCard):
    id: int = 311207
    name: str = "End of the Line"
    name_ch = "竭泽"
    weapon_type: WeaponType = WeaponType.BOW
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = EndoftheLineWeapon
    
    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
