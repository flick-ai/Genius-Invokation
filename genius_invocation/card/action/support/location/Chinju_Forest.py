from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Chinju_Forest_Entity(Support):
    id: int = 32101261
    name = 'Chinju Forest'
    name_ch = '镇守之森'
    max_usage = 3
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.first_player != self.from_player.index:
                dice_type = ElementToDice[get_my_active_character(game).element]
                self.from_player.dice_zone.add([dice_type.value])
                self.usage -= 1
                if self.usage == 0:
                    self.on_destroy(self)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]

    def show(self):
        return str(self.usage)

class Chinju_Forest(SupportCard):
    '''
        镇守之森
    '''
    id: int = 321013
    name: str = 'Chinju Forest'
    name_ch = '镇守之森'
    time = 3.7
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Chinju_Forest_Entity(game, from_player=game.active_player)
        super().on_played(game)