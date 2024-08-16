from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from genius_invocation.card.action.base import ActionCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Combat_Status
from copy import deepcopy

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class SirArthurEntity(Support):
    name: str = 'Sir Arthur'
    name_ch = '亚瑟先生'
    id = 32202661
    max_count = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.news_lead = 0

    def on_tune_card(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.news_lead = min(self.max_count, self.news_lead + 1)

    def on_discard_card(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.news_lead = min(self.max_count, self.news_lead + 1)

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.news_lead == self.max_count:
                self.news_lead = 0
                card = get_opponent(game).card_zone.card[0]
                self.from_player.hand_zone.add([deepcopy(card)])

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_TUNE_CARD, ZoneType.SUPPORT_ZONE, self.on_tune_card),
            (EventType.ON_DISCARD_CARD, ZoneType.SUPPORT_ZONE, self.on_discard_card),
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]

class SirArthur(SupportCard):
    id: int = 322026
    name: str = 'Sir Arthur'
    name_ch = '亚瑟先生'
    time = 4.7
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = SirArthurEntity(game, from_player=game.active_player)
        super().on_played(game)



