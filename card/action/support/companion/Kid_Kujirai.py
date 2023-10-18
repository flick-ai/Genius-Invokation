from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Kid_Kujirai_Entity(Support):
    id: int = 322014
    name = 'Kid Kujirai'
    max_usage = -1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.cleansing_ritual_progress = 0

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.dice_zone.add([DiceType.OMNI.value])
            opponent = get_opponent(game)
            if not opponent.support_zone.check_full():
                self.from_player.support_zone.destroy(self)
                opponent.support_zone.add_entity(self, -1)
                self.from_player = opponent

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Kid_Kujirai(SupportCard):
    '''
        鲸井小弟
    '''
    id: int = 322014
    name: str = 'Kid Kujirai'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Kid_Kujirai_Entity(game, from_player=game.active_player)
        super().on_played(game)
