from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class AteaEntity(Support):
    id: int = 32202861
    name = 'Atea'
    name_ch = '阿伽娅'
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = 1

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == SkillType.SPECIAL_SKILL:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0:
                        game.current_dice.cost[0]['cost_num'] -= 1
                        return True
                    if len(game.current_dice.cost)>1:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_special_skill(self, game:'GeniusGame'):
        if self.on_calculate(game):
            self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin),
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.ON_USE_SPECIAL, ZoneType.SUPPORT_ZONE, self.on_special_skill)
        ]


class Atea(SupportCard):
    id: int = 322028
    name: str = 'Atea'
    name_ch = '阿伽娅'
    time = 5.0
    cost_num = 1
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = AteaEntity(game, game.active_player)
        super().on_played(game)
