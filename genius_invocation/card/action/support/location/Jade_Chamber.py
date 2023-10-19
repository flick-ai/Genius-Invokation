from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from loguru import logger

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Jade_Chamber_Entity(Support):
    id: int = 321003
    name = 'Jade Chamber'
    max_usage = -1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            dice_type = ElementToDice[get_my_active_character(game).element]
            self.from_player.fix_dice += [dice_type.value, dice_type.value,]
            logger.info(f"Jade_Chamber:fix dice {[dice_type.value, dice_type.value,]}")

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ROLL_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Jade_Chamber(SupportCard):
    '''
        群玉阁
    '''
    id: int = 321003
    name: str = 'Jade Chamber'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Jade_Chamber_Entity(game, from_player=game.active_player)
        super().on_played(game)