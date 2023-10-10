from utils import *
from game.game import GeniusGame
from ..base import ActionCard


class SupportCard(ActionCard):
    # 支援牌基本类
    def __init__(self) -> None:
        super().__init__()