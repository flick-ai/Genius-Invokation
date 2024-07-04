from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support
from genius_invocation.entity.status import Status

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Sand_and_Dreams(Status):
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1
        self.cost = 3

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            is_use = False
            if game.current_dice.use_type in SkillType:
                if game.current_dice.cost[0]['cost_num']>0 and self.usage > 0:
                    new_cost = max(0, game.current_dice.cost[0]['cost_num']-self.cost)
                    self.cost = max(0, self.cost-game.current_dice.cost[0]['cost_num'])
                    game.current_dice.cost[0]['cost_num'] = new_cost
                    is_use = True
                if len(game.current_dice.cost)>1:
                    if game.current_dice.cost[1]['cost_num'] > 0 and self.usage > 0:
                        new_cost = max(0, game.current_dice.cost[1]['cost_num']-self.cost)
                        self.cost = max(0, self.cost-game.current_dice.cost[1]['cost_num'])
                        game.current_dice.cost[1]['cost_num']  = new_cost
                        is_use =  True
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_TALENT:
                if game.current_dice.cost[0]['cost_num']>0 and self.usage > 0:
                    new_cost = max(0, game.current_dice.cost[0]['cost_num']-self.cost)
                    self.cost = max(0, self.cost-game.current_dice.cost[0]['cost_num'])
                    game.current_dice.cost[0]['cost_num'] = new_cost
                    is_use = True
                if len(game.current_dice.cost)>1:
                    if game.current_dice.cost[1]['cost_num'] > 0 and self.usage > 0:
                        new_cost = max(0, game.current_dice.cost[1]['cost_num']-self.cost)
                        self.cost = max(0, self.cost-game.current_dice.cost[1]['cost_num'])
                        game.current_dice.cost[1]['cost_num']  = new_cost
                        is_use =  True
        return is_use

    def on_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)

    def on_play(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_skill),
            (EventType.ON_PLAY_CARD, ZoneType.SUPPORT_ZONE, self.on_play),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
        ]


class Jeht_Entity(Support):
    id: int = 322022
    name: str = 'Jeht'
    name_ch = '婕德'
    max_usage = -1
    max_count = 6
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.sophistication = self.from_player.support_zone.distroy_count

    def on_support_remove(self, game:'GeniusGame'):
        self.sophistication = self.from_player.support_zone.distroy_count

    def on_after_skill(self, game:'GeniusGame'):
        if self.sophistication == self.max_count:
            if game.current_skill.type == SkillType.ELEMENTAL_BURST:
                get_my_active_character(game).character_zone.add_entity(
                    Sand_and_Dreams(game, game.active_player, get_my_active_character(game))
                )
                self.on_destroy(game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_SUPPORT_REMOVE, ZoneType.SUPPORT_ZONE, self.on_support_remove),
            (EventType.AFTER_USE_SKILL, ZoneType.SUPPORT_ZONE, self.on_after_skill),
        ]

    def show(self):
        return str(self.sophistication)


class Jeht(SupportCard):
    id: int = 322022
    name: str = 'Jeht'
    name_ch = '婕德'
    time = 4.4
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Jeht_Entity(game, from_player=game.active_player)
        super().on_played(game)
    
    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.6] = "调整了支援牌「婕德」所需元素骰和效果：所需元素骰由2个任意元素骰调整为1个元素骰；效果“如果「阅历」至少为5，则弃置此牌，生成「阅历」-2数量的万能元素。”调整为“如果「阅历」至少为6，则弃置此牌，对我方出战角色附属沙与梦。”（「沙与梦」效果为：“对角色打出「天赋」或角色使用技能时：少花费3个元素骰”）"
        return log
