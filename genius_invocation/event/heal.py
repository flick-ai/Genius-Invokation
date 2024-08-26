from typing import TYPE_CHECKING
from genius_invocation.utils import *
from genius_invocation.event.Elemental_Reaction import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame

class Heal:
    def __init__(
            self,
            heal: int,
            target_character: 'Character',
            heal_type: HealType = HealType.HEAL
            ) -> None:
        self.heal_to_character = target_character
        self.heal_to_player = target_character.from_player
        self.heal_num = heal
        self.heal_type = heal_type

class BondofLife(Status):
    id: int = 23
    name: str = "Bond of Life"
    name_ch = "生命之契"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None, usgae=1):
        super().__init__(game, from_player, from_character)
        self.usage = usgae

    def update(self, usage=1):
        self.usage += usage

    def on_heal(self, game: 'GeniusGame'):
        if game.current_heal.heal_to_character == self.from_character:
            if game.current_heal.heal_type in [HealType.HEAL, HealType.MAX_HEALTH]:
                target_heal = max(0, game.current_heal.heal_num - self.usage)
                self.usage = max(0, self.usage - game.current_heal.heal_num)
                game.current_heal.heal_num = target_heal
                if self.usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_HEAL, ZoneType.CHARACTER_ZONE, self.on_heal)
        ]

    def balance_adjustment():
        log = {}
        log[5.0] = "可以抵消最大生命值治疗效果"
        return log




