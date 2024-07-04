from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Dunyarzad_Entity(Support):
    id: int = 322016
    name = 'Dunyarzad'
    name_ch = '迪娜泽黛'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage_round = self.max_usage
        self.usage_game = self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage_round = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage_round > 0:
                if game.current_dice.use_type == ActionCardType.SUPPORT_COMPANION:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] = max(0,  game.current_dice.cost[0]['cost_num']-1)
                        return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage_round -= 1
        if game.active_player_index == self.from_player.index:
            if self.usage_game > 0:
                if game.current_dice.use_type == ActionCardType.SUPPORT_COMPANION:
                    card = self.from_player.card_zone.find_card(ActionCardType.SUPPORT_COMPANION)
                    self.from_player.hand_zone.add(card)
                    self.usage_game -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
        ]
    def show(self):
        if self.usage_round>0:
            return "^v^"
        else:
            return "-_-"



class Dunyarzad(SupportCard):
    '''
        迪娜泽黛
    '''
    id: int = 322016
    name: str = 'Dunyarzad'
    name_ch = '迪娜泽黛'
    time = 3.7
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Dunyarzad_Entity(game, from_player=game.active_player)
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.1] = "支援牌「迪娜泽黛」增加了额外的效果：首次触发效果后，还会从牌组中随机抽取一张「伙伴」支援牌"
        return log
