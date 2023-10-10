from utils import *
from game.game import GeniusGame


class ActionCard:
    # 行动牌基本类
    id: int
    name: str
    cost_num: int
    cost_type: CostType

    def effect(self, game: GeniusGame) -> None:
        '''
            效果执行函数
        '''
