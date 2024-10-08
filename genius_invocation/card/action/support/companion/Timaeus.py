from genius_invocation.utils import *
from genius_invocation.card.action.support.base import SupportCard
from typing import TYPE_CHECKING
from genius_invocation.entity.support import Support

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class Timaeus_Entity(Support):
    id: int = 32200361
    name = 'Timaeus'
    name_ch = '蒂玛乌斯'
    max_usage = 1
    max_count = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.usage = self.max_usage
        self.transmutation_material = 2

    def on_calculate(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if game.current_dice.use_type == ActionCardType.EQUIPMENT_ARTIFACT:
                if self.usage > 0:
                    if game.current_dice.cost[0]['cost_num'] > 0 and game.current_dice.cost[0] <= self.transmutation_material:
                        need = game.current_dice.cost[0]['cost_num']
                        game.current_dice.cost[0]['cost_num'] = 0
                        return need
        return False

    def on_use(self, game:'GeniusGame'):
        use = self.on_calculate(game)
        if use != False:
            self.usage -= 1
            self.transmutation_material -= use

    def on_begin(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.usage = self.max_usage

    def on_end(self, game:'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            self.transmutation_material += 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.CALCULATE_DICE, ZoneType.SUPPORT_ZONE, self.on_calculate),
            (EventType.END_PHASE, ZoneType.SUPPORT_ZONE, self.on_end),
            (EventType.ON_CHANGE_CHARACTER, ZoneType.SUPPORT_ZONE, self.on_use),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.SUPPORT_ZONE, self.on_begin)
        ]

    def show(self):
        return str(self.transmutation_material)

class Timaeus(SupportCard):
    '''
        蒂玛乌斯
    '''
    id: int = 322003
    name: str = 'Timaeus'
    name_ch = '蒂玛乌斯'
    cost_num = 2
    cost_type = CostType.WHITE
    card_type = ActionCardType.SUPPORT_COMPANION

    def __init__(self) -> None:
        super().__init__()
        self.entity = None

    def on_played(self, game: 'GeniusGame') -> None:
        self.entity = Timaeus_Entity(game, from_player=game.active_player)
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[4.3] = "支援牌「蒂玛乌斯」新增效果：“入场时：如果我方牌组中初始包含至少6张「圣遗物」，则从牌组中随机抽取1张「圣遗物」牌”"
        return log
