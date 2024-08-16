from genius_invocation.utils import *
from genius_invocation.card.action.equipment.weapon.base import WeaponCard
from typing import TYPE_CHECKING
from genius_invocation.entity.status import Weapon

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class MagicSwordWeapon(Weapon):
    id: int = 31130881
    name: str = "Ultimate Overlord's Mega Magic Sword"
    name_ch = "「究极霸王超级魔剑」"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, weapon_card = None):
        super().__init__(game, from_player, from_character, weapon_card)
        self.support = 0
        for card_name in from_player.played_cards:
            if card_name not in self.from_player.card_zone.card_name:
                self.support += 1

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            if self.support >= 8:
                game.current_damage.damage += 3
            elif self.support >= 4:
                game.current_damage.damage += 2
            elif self.support >= 2:
                game.current_damage.damage += 1

    def on_play_card(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_card.name not in self.from_player.card_zone.card_name:
                self.support += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage),
            (EventType.AFTER_PLAY_CARD, ZoneType.CHARACTER_ZONE, self.on_play_card),
        ]


class MagicSword(WeaponCard):
    id: int = 311308
    name: str = "Ultimate Overlord's Mega Magic Sword"
    name_ch = "「究极霸王超级魔剑」"
    time = 4.8
    weapon_type: WeaponType = WeaponType.CLAYMORE
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.equipment_entity = MagicSwordWeapon

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
