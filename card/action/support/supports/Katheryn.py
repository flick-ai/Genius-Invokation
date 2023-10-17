from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Katheryn_Entity(Support):
    id: int = 322002
    name = 'Katheryn'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_change(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            if self.from_player.is_quick_change == False:
                if self.usage > 0:
                    self.from_player.is_quick_change == True

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            self.usage = self.max_usage


    def update_listener_list(self):
        self.listeners = [
            (EventType.BEFORE_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_change),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Katheryn(SupportCard):
    id: int = 322002
    name: str = 'Katheryn'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Katheryn_Entity(game, from_player=game.active_player)
        super().on_played
