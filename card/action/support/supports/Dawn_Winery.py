from utils import *
from ..base import SupportCard
from typing import TYPE_CHECKING
from entity.support import Support

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.player import GeniusPlayer


class Dawn_Winery_Entity(Support):
    id: int = 321004
    name = 'Dawn Wineryr'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            if game.current_dice.use_type == 'change_character':
                if self.usage > 0:
                    if game.current_dice.cost[0] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
        return False

    def on_use(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.idx:
            self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_use),
        ]


class Dawn_Winery(SupportCard):
    id: int = 321004
    name: str = 'Dawn Winery'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Dawn_Winery_Entity(game, from_player=game.active_player)
        super().on_played