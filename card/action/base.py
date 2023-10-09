from utils import *
from typing import List
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


class EquipmentCard(ActionCard):
    # 装备牌基本类
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame) -> None:
        raise NotImplementedError

class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type: WeaponType
    
    def effect(self, game: GeniusGame) -> None:
        pass 

    def on_played(self, game: GeniusGame) -> None:
        target = game.current_action.choice_idx
        game.players[game.active_player].active_zone.character_list[target].weapon_card = self


class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()
