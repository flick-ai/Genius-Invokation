from entity.entity import Entity
from utils import *
from game.game import GeniusGame
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.action import Action
    from event.events import ListenerNode
    from game.player import GeniusPlayer

from entity.character import Character
from entity.status import Status


class Electro_Infusion(Status):
    max_usage = 2
    def __init__(self, game, from_player: GeniusPlayer, from_character=None):
        super().__init__(game, from_player, from_character)
        usage = 0

    def infuse(self, game: GeniusGame):
        if game.current_damage.damage_from == self.from_character:
            if game.current_damage.main_damage_element == ElementType.PHYSICAL:
                game.current_damage.main_damage_element = ElementType.ELECTRO

    def on_end_phase(self, game:GeniusGame):
        self.usage -= 1
        if self.usage <= 0:
            self.on_destroy(game)
    
    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end_phase),
            (EventType.INFUSION, ZoneType.CHARACTER_ZONE, self.infuse)
        ]
        