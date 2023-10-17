from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Liyue_Harbor_Wharf_Entity(Support):
    id: int = 322001
    name = 'Liyue Haroboe Wharf'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            self.from_player.get_card(num=2)
            self.usage -= 1
            if self.usage == 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Liyue_Harbor_Wharf(SupportCard):
    '''
        璃月港口
    '''
    id: int = 321001
    name: str = 'Liyue Harbor Wharf'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Liyue_Harbor_Wharf_Entity(game, from_player=game.active_player)
        super().on_played(game)