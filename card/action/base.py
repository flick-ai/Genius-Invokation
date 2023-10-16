from typing import TYPE_CHECKING
from utils import *

if TYPE_CHECKING:
    from game.game import GeniusGame


class ActionCard:
    # 行动牌基本类
    id: int
    name: str
    cost_num: int
    cost_type: CostType
    card_type: ActionCardType

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
        active_dice = ElementToDice(get_my_active_character(game).element).value
        game.active_player.dice_zone.add([active_dice])
