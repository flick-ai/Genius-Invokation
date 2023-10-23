from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from loguru import logger
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Paimon_Entity(Support):
    id: int = 322001
    name = 'Paimon'
    name_ch = '派蒙'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.dice_zone.add([DiceType.OMNI.value, DiceType.OMNI.value,])
            self.usage -= 1
            logger.info(f"Paimon:{self.from_player.dice_zone.num()},剩余使用次数{self.usage}")
            if self.usage == 0:
                logger.info(f"Paimon Destroy")
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return str(self.usage)

class Paimon(SupportCard):
    '''
        派蒙
    '''
    id: int = 322001
    name: str = 'Paimon'
    name_ch = '派蒙'
    cost_num = 3
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Paimon_Entity(game, from_player=game.active_player)
        super().on_played(game)
