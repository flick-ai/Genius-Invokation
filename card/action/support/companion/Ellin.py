from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Ellin_Entity(Support):
    id: int = 322010
    name = 'Ellin'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage > 0:
                if game.current_skill.usage_this_round > 1:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if game.current_dice.cost[1]['cost_num'] > 0:
                        game.current_dice.cost[1]['cost_num'] -= 1
                        return True

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
           self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUMMON_ZONE, self.on_begin)
        ]
    
    def show(self):
        if self.usage > 0:
            return "^v^"
        else:
            return "-_-"


class Ellin(SupportCard):
    '''
        艾琳
    '''
    id: int = 322010
    name: str = 'Ellin'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Ellin_Entity(game, from_player=game.active_player)
        super().on_played(game)
