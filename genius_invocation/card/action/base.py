from typing import TYPE_CHECKING
from genius_invocation.utils import *

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class ActionCard:
    # 行动牌基本类
    id: int
    name: str
    name_ch: str = ""
    cost_num: int
    cost_type: CostType
    card_type: ActionCardType
    can_tune: bool = True

    def calculate_dice(self, game: 'GeniusGame') -> int:
        if self.cost_type == ActionCardType.EQUIPMENT_TALENT:
            count = sum([i['cost_num'] for i in self.cost])
        else:
            count = self.cost_num
        return count

    def on_played(self, game: 'GeniusGame') -> None:
        '''
            效果执行函数
        '''
        pass

    def find_target(self, game: 'GeniusGame'):
        '''
            寻找目标函数
        '''
        return [1]

    def on_tuning(self, game: 'GeniusGame'):
        '''
            元素调和函数
        '''
        active_dice = ElementToDice[get_my_active_character(game).element].value
        game.active_player.dice_zone.add([active_dice])

    def on_discard(self, game: 'GeniusGame'):
        '''
            弃牌函数
        '''
        pass
