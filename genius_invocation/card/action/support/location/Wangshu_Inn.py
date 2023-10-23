from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
import numpy as np

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Wangshu_Inn_Entity(Support):
    id: int = 321005
    name = 'Wangshu Inn'
    name_ch = '望舒客栈'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            injured = np.zeros(2)
            standby_character = get_my_standby_character(game)
            for idx, character in enumerate(standby_character):
                injured[idx] = character.max_health_point - character.health_point
            max_injured = injured.argmax()
            if injured.max() > 0:
                standby_character[max_injured].heal(heal=2)
                self.usage -= 1
                if self.usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
        ]
    def show(self):
        return str(self.usage)

class Wangshu_Inn(SupportCard):
    '''
        望舒客栈
    '''
    id: int = 321005
    name: str = 'Wangshu Inn'
    name_ch = '望舒客栈'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Wangshu_Inn_Entity(game, from_player=game.active_player)
        super().on_played(game)