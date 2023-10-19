from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Grand_Narukami_Shrine_Entity(Support):
    id: int = 321008
    name = 'Grand Narukami Shrine'
    max_usage = 3
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.from_player.dice_zone.add(self.from_player.roll_dice(num=1, is_basic=True))
        self.usage = self.max_usage - 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.from_player.dice_zone.add(self.from_player.roll_dice(num=1, is_basic=True))
            self.usage -= 1
            if self.usage == 0:
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return str(self.usage)


class Grand_Narukami_Shrine(SupportCard):
    '''
        鸣神大社
    '''
    id: int = 321008
    name: str = 'Grand Narukami Shrine'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Grand_Narukami_Shrine_Entity(game, from_player=game.active_player)
        super().on_played(game)