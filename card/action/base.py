from utils import *
from typing import List
from game.game import GeniusGame


class ActionCard:
    # 行动牌基本类
    def __init__(self) -> None:
        self.id: int
        self.name: str

    def on_played(self, game: GeniusGame) -> None:
        raise NotImplementedError


class EquipmentCard(ActionCard):
    # 装备牌基本类
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame, target) -> None:
        pass


class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()
