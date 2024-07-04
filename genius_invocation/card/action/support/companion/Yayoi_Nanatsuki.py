from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Yayoi_Nanatsuki_Entity(Support):
    id: int = 322020
    name = 'Yayoi_Nanatsuki'
    name_ch = '弥生七月'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage= self.max_usage

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage > 0:
                if game.current_dice.use_type == ActionCardType.EQUIPMENT_ARTIFACT:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        artifact_num = 0
                        for character in self.from_player.character_list:
                            if character.character_zone.artifact_card != None:
                                artifact_num += 1
                        game.current_dice.cost[0]['cost_num'] = max(0, game.current_dice.cost[0]['cost_num']-1-artifact_num)
                        return True
        return False

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
        ]
    def show(self):
        if self.usage>0:
            return '^v^'
        else:
            return '-_-'


class Yayoi_Nanatsuki(SupportCard):
    '''
        弥生七月
    '''
    id: int = 322020
    name: str = 'Yayoi Nanatsuki'
    name_ch = '弥生七月'
    time = 4.1
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Yayoi_Nanatsuki_Entity(game, from_player=game.active_player)
        super().on_played(game)
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.6] = "调整了支援牌「弥生七月」的效果：”如果我方场上每有一个已装备「圣遗物」的角色，就额外少花费1个元素骰。”调整为“如果我方场上已有2个已装备「圣遗物」的角色，就额外少花费1个元素骰。””"
        return log
