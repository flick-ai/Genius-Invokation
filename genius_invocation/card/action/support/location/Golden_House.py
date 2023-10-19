from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Golden_House_Entity(Support):
    id: int = 321013
    name = 'Golden House'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage
        self.usage_round = 1

    def on_calculate(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_WEAPON or game.current_dice.use_type == ActionCardType.EQUIPMENT_ARTIFACT:
                if game.current_dice.origin_cost[0]['cost_num']>=3:
                    if self.usage_round > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
        return False

    def on_play(self, game: 'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1
            self.usage_round -= 1
            if self.usage == 0:
                self.on_destroy(game)

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage_round = 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        return str(self.usage)

class Golden_House(SupportCard):
    '''
        黄金屋
    '''
    id: int = 321013
    name: str = 'Golden House'
    cost_num = 0
    cost_type = None
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Golden_House_Entity(game, from_player=game.active_player)
        super().on_played(game)