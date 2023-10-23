from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Liu_Su_Entity(Support):
    id: int = 322012
    name = 'Liu Su'
    name_ch = '刘苏'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage
        self.usage_round = 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage_round = 1

    def on_change(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage_round > 0:
                character = self.from_player.character_list[self.from_player.active_idx]
                if character.power == 0:
                    character.power += 1
                    self.usage_round -= 1
                    self.usage -= 1
                    if self.usage == 0:
                        self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_change),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin)
        ]

    def show(self):
        st = "-_-"
        if self.usage_round:
            st = "^v^"
        return str(self.usage) + " " + st

class Liu_Su(SupportCard):
    '''
        刘苏
    '''
    id: int = 322012
    name: str = 'Liu Su'
    name_ch = '刘苏'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Liu_Su_Entity(game, from_player=game.active_player)
        super().on_played(game)
