from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Knights_of_Favonius_Library_Entity(Support):
    id: int = 32100261
    name = 'Knights of Favonius Library'
    name_ch = '骑士团图书馆'
    max_usage = -1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.roll_time += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ROLL_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return '┬─┬┬─┬'

class Knights_of_Favonius_Library(SupportCard):
    '''
        骑士团图书馆
    '''
    id: int = 321002
    name: str = 'Knights of Favonius Library'
    name_ch = '骑士团图书馆'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None
        self.now_phase: GamePhase

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Knights_of_Favonius_Library_Entity(game, from_player=game.active_player)
        super().on_played(game)
        self.now_phase = game.game_phase
        game.game_phase = GamePhase.ROLL_PHASE
        game.active_player.roll_time = 1
        game.special_phase = self

    def on_finished(self, game: 'GeniusGame'):
        game.game_phase = self.now_phase
        game.special_phase = None
        game.resolve_action(None)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.5] = "调整了支援牌「骑士团图书馆」所需元素骰：所需元素骰由1个调整为0个"
        return log