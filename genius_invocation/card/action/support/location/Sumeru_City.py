from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Sumeru_City_Entity(Support):
    id: int = 321010
    name = 'Sumeru City'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type in SkillType:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if len(game.current_dice.cost)>1:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_TALENT:
                 if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if game.current_dice.cost[1]['cost_num'] > 0:
                        game.current_dice.cost[1]['cost_num'] -= 1
                        return True
        return False

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]

    def show(self):
        if self.usage>0:
            return '┬─┬┬─┬'
        else:
            return '(╯°□°）╯︵ ┻━┻┻━┻'
class Sumeru_City(SupportCard):
    '''
        须弥城
    '''
    id: int = 321010
    name: str = 'Sumeru City'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Sumeru_City_Entity(game, from_player=game.active_player)
        super().on_played(game)