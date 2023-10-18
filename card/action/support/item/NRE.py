from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class NRE_Entity(Support):
    id: int = 323002
    name = 'NRE'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        card = self.from_player.card_zone.find_card(card_type=ActionCardType.EVENT_FOOD)
        self.from_player.hand_zone.add([card])
        self.usage = self.max_usage

    def on_play(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EVENT_FOOD:
                if self.usage > 0:
                    card = self.from_player.card_zone.find_card(card_type=ActionCardType.EVENT_FOOD)
                    self.from_player.hand_zone.add([card])
                    self.usage -= 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class NRE(SupportCard):
    '''
        便携营养袋
    '''
    id: int = 323002
    name: str = 'NRE'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = NRE_Entity(game, from_player=game.active_player)
        super().on_played(game)
