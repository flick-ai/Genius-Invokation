from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Gandharva_Ville_Entity(Support):
    id: int = 321014
    name = 'Gandharva Ville'
    max_usage = 3
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_before(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.from_player.dice_zone.num() == 0:
                self.from_player.dice_zone.add([DiceType.OMNI.value])
                self.usage -= 1
                if self.usage == 0:
                    self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEFORE_ANY_ACTION, ZoneType.SUPPORT_ZONE, self.on_before),
        ]
    def show(self):
        return str(self.usage)

class Gandharva_Ville(SupportCard):
    '''
        化城郭
    '''
    id: int = 321014
    name: str = 'Gandharva Ville'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Gandharva_Ville_Entity(game, from_player=game.active_player)
        super().on_played(game)