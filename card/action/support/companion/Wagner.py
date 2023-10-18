from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Wagner_Entity(Support):
    id: int = 322004
    name = 'Wagner'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage
        self.forging_billets  = 2

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_WEAPON:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0 and game.current_dice.cost[0] <= self.forging_billets :
                        game.current_dice.cost[0]['cost_num'] = 0
                        return game.current_dice.cost[0]
        return False

    def on_use(self, game:'GeniusGame'):
        use = self.on_calculate(game)
        if use != False:
            self.usage -= 1
            self.forging_billets  -= use

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.forging_billets  += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_use),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin)
        ]

class Wagner(SupportCard):
    '''
        瓦格纳
    '''
    id: int = 322004
    name: str = 'Wagner'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Wagner_Entity(game, from_player=game.active_player)
        super().on_played(game)
