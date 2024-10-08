from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Chef_Mao_Entity(Support):
    id: int = 322005
    name = 'Chef Mao'
    name_ch = '卯师傅'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage_round = self.max_usage
        self.usage_game = self.max_usage

    def on_after(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EVENT_FOOD:
                if self.usage_round > 0:
                    self.from_player.dice_zone.add(self.from_player.roll_dice(num=1, is_basic=True))
                    self.usage_round -= 1
                if self.usage_game > 0:
                    card = self.from_player.card_zone.find_card(card_type=ActionCardType.EVENT_FOOD, random_choice=True)
                    self.from_player.hand_zone.add(card)
                    self.usage_game = 0 # only once per support

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage_round = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.AFTER_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_after)
        ]
    def show(self):
        if self.usage_round>0:
            return "^v^"
        else:
            return "-_-"

class Chef_Mao(SupportCard):
    '''
        卯师傅
    '''
    id: int = 322005
    name: str = 'Chef Mao'
    name_ch = '卯师傅'
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Chef_Mao_Entity(game, from_player=game.active_player)
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "支援牌「卯师傅」增加了额外的效果：首次触发效果后，还会从牌组中随机抽取一张「料理」事件牌"
