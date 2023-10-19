from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Parametric_Transformer_Entity(Support):
    id: int = 323001
    name = 'Parametric Transformer'
    max_usage = -1
    max_count = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.qualitative_progress = 0

    def on_after(self, game:'GeniusGame'):
        self.qualitative_progress += 1
        if self.qualitative_progress == self.max_count:
            self.from_player.dice_zone.add(self.from_player.roll_dice(num=3, is_basic=True, is_different=True))
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_after),
        ]
    def show(self):
        return str(self.qualitative_progress)

class Parametric_Transformer(SupportCard):
    '''
        参量质变仪
    '''
    id: int = 323001
    name: str = 'Parametric Transformer'
    cost_num = 2
    cost_type = CostType.BLACK
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Parametric_Transformer_Entity(game, from_player=game.active_player)
        super().on_played(game)
