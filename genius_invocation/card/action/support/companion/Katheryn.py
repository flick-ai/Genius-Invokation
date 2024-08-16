from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Katheryn_Entity(Support):
    id: int = 32200261
    name = 'Katheryn'
    name_ch = '凯瑟琳'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_change(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.from_player.is_quick_change == False:
                if self.usage > 0:
                    self.from_player.is_quick_change == True

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage


    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_change),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]

    def show(self):
        if self.usage > 0:
            return "^v^"
        else:
            return "-_-"

class Katheryn(SupportCard):
    '''
        凯瑟琳
    '''
    id: int = 322002
    name: str = 'Katheryn'
    name_ch = '凯瑟琳'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Katheryn_Entity(game, from_player=game.active_player)
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.6] = "调整了「七圣召唤」中，事件牌「凯瑟琳」所需元素骰子数量：所需骰子数量由2个任意元素骰子调整为1个骰子"
        return log
