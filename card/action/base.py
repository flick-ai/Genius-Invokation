from utils import *
from game.game import GeniusGame


class ActionCard:
    # 行动牌基本类
    id: int
    name: str
    cost_num: int
    cost_type: CostType

    def play(self, game: GeniusGame) -> None:
        '''
        pre played
        on played
        post played
        '''
        self.pre_played(game)
        self.on_played(game)
        self.post_played(game)

    def pre_played(self, game: GeniusGame) -> None:
        pass 

    def post_played(self, game: GeniusGame) -> None:
        pass

    def on_played(self, game: GeniusGame) -> None:
        raise NotImplementedError

