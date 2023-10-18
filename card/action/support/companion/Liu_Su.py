from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Liu_Su_Entity(Support):
    id: int = 322012
    name = 'Liu Su'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage
        self.usage_round = 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]


class Liu_Su(SupportCard):
    '''
        刘苏
    '''
    id: int = 322012
    name: str = 'Liu Su'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Liu_Su_Entity(game, from_player=game.active_player)
        super().on_played(game)
