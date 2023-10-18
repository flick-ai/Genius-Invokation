from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Knights_of_Favonius_Library_Entity(Support):
    id: int = 321002
    name = 'Knights of Favonius Library'
    max_usage = -1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_character.roll_time += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ROLL_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]


class Knights_of_Favonius_Library(SupportCard):
    '''
        骑士团图书馆
    '''
    id: int = 321002
    name: str = 'Knights of Favonius Library'
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