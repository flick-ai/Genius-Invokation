from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Setaria_Entity(Support):
    id: int = 322019
    name = 'Setaria'
    max_usage = 3
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_after(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.from_player.hand_zone.num() == 0:
                self.from_player.get_card(num=1)
                self.usage -= 1
                if self.usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_ANY_ACTION, ZoneType.SUPPORT_ZONE, self.on_after),
        ]


class Setaria(SupportCard):
    '''
        塞塔蕾
    '''
    id: int = 322019
    name: str = 'Setaria'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Setaria_Entity(game, from_player=game.active_player)
        super().on_played(game)
