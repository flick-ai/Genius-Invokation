from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Timmie_Entity(Support):
    id: int = 322007
    name = 'Timmie'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.pigeon = 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.pigeon += 1
            if self.pigeon == self.max_usage:
                self.from_player.dice_zone.add([DiceType.OMNI.value])
                self.from_player.get_card(num=1)
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Timmie(SupportCard):
    '''
        提米
    '''
    id: int = 322007
    name: str = 'Timmie'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Timmie_Entity(game, from_player=game.active_player)
        super().on_played(game)
