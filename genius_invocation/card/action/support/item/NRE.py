from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class NRE_Entity(Support):
    id: int = 32300261
    name = 'NRE'
    name_ch = '便携营养袋'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        card = self.from_player.card_zone.find_card(card_type=ActionCardType.EVENT_FOOD)
        self.from_player.hand_zone.add([card])
        self.usage = self.max_usage

    def on_play(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EVENT_FOOD:
                if self.usage > 0:
                    card = self.from_player.card_zone.find_card(card_type=ActionCardType.EVENT_FOOD)
                    self.from_player.hand_zone.add([card])
                    self.usage -= 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
        ]
    def show(self):
        if self.usage>0:
            return '┬─┬┬─┬'
        else:
            return '(╯°□°）╯︵ ┻━┻┻━┻'


class NRE(SupportCard):
    '''
        便携营养袋
    '''
    id: int = 323002
    name: str = 'NRE'
    name_ch = '便携营养袋'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_ITEM

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = NRE_Entity(game, from_player=game.active_player)
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "调整了支援牌「便携营养袋」所需元素骰费用：所需元素骰调整为1个元素骰"
        return log
