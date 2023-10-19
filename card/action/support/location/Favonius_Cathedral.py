from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support
import numpy as np

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Favonius_Cathedral_Entity(Support):
    id: int = 321006
    name = 'Favonius Cathedral'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            activte_character = get_active_character(game)
            if activte_character.health_point != activte_character.max_health_point:
                activte_character.heal(heal=2)
                self.usage -= 1
                if self.usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]
    def show(self):
        return str(self.usage)


class Favonius_Cathedral(SupportCard):
    '''
        西风大教堂
    '''
    id: int = 321006
    name: str = 'Favonius Cathedral'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Favonius_Cathedral_Entity(game, from_player=game.active_player)
        super().on_played(game)