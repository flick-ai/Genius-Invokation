from utils import *
from game.game import GeniusGame
from ..base import EquipmentCard


class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type: WeaponType
    
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: GeniusGame) -> None:
        super().on_played(game)
        self.character.weapon_card = self