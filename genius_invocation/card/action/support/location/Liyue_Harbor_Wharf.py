from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from loguru import logger

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Liyue_Harbor_Wharf_Entity(Support):
    id: int = 322001
    name = 'Liyue Haroboe Wharf'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.get_card(num=2)
            self.usage -= 1
            logger.info(f"Liyue_Harbor_Wharf:{self.from_player.hand_zone.num()},剩余使用次数{self.usage}")
            if self.usage == 0:
                logger.info(f"Liyue_Harbor_Wharf Destroy")
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