from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Tenshukaku_Entity(Support):
    id: int = 32100761
    name = 'Tenshukaku'
    name_ch = '天守阁'
    time = 3.7
    max_usage = -1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            dices = self.from_player.dice_zone.space[:, :-1]
            types = [i>0 for i in [dices.sum(axis=0)-dices[:, -1].sum(axis=0)]][0].sum() + dices[:, -1].sum(axis=0)
            if types >= 5:
                self.from_player.dice_zone.add([DiceType.OMNI.value])

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return '┬─┬┬─┬'

class Tenshukaku(SupportCard):
    '''
        天守阁
    '''
    id: int = 321007
    name: str = 'Tenshukaku'
    name_ch = '天守阁'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Tenshukaku_Entity(game, from_player=game.active_player)
        super().on_played(game)