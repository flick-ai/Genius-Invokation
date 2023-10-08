from utils import *
from typing import List
from game.game import GeniusGame


class ActionCard:
    # 行动牌基本类
    id: int
    name: str
    cost_num: int
    cost_type: CostType

    def on_played(self, game: GeniusGame) -> None:
        raise NotImplementedError


class EquipmentCard(ActionCard):
    # 装备牌基本类
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame, target) -> None:
        pass

class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type: WeaponType
    
    def effect(game: GeniusGame) -> None:
        pass 
    
    def on_played(self, game: GeniusGame, target) -> None:
        return super().on_played(game, target)


class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()
