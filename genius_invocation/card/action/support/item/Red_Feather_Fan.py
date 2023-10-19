from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Red_Feather_Fan_Entity(Support):
    id: int = 323003
    name = 'Red Feather Fan'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == 'change character':
                if self.usage > 0:
                    if self.from_player.change_num%2 == 0:
                        if game.current_dice.cost[0] > 0 and self.from_player.is_quick_change == False:
                            game.current_dice.cost[0]['cost_num'] -= 1
                            return True
        return False

    def on_change(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1
            self.from_player.is_quick_change = True

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_change),
        ]
    def show(self):
        if self.usage>0:
            return '┬─┬┬─┬'
        else:
            return '(╯°□°）╯︵ ┻━┻┻━┻'


class Red_Feather_Fan(SupportCard):
    '''
        红羽团扇
    '''
    id: int = 323003
    name: str = 'Red Feather Fan'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Red_Feather_Fan_Entity(game, from_player=game.active_player)
        super().on_played(game)
