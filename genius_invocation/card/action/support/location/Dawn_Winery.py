from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Dawn_Winery_Entity(Support):
    id: int = 32100461
    name = 'Dawn Wineryr'
    name_ch = '晨曦酒庄'
    max_usage = 2
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SwitchType.CHANGE_CHARACTER:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
        return False

    def on_use(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_use),
        ]

    def show(self):
        if self.usage>0:
            return '┬─┬┬─┬'
        else:
            return '(╯°□°）╯︵ ┻━┻┻━┻'


class Dawn_Winery(SupportCard):
    '''
        晨曦酒庄
    '''
    id: int = 321004
    name: str = 'Dawn Winery'
    name_ch = '晨曦酒庄'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_LOCATION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Dawn_Winery_Entity(game, from_player=game.active_player)
        super().on_played(game)

    def balance_adjustment():
        log = {
            4.8:"调整了支援牌「晨曦酒庄」的效果：效果触发的限制“每回1次”调整为“每回合至多2次”",
        }
        return log