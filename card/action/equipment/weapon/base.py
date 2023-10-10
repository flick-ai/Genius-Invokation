from utils import *
from game.game import GeniusGame
from ..base import EquipmentCard


class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type: WeaponType
    def __init__(self) -> None:
        super().__init__()
        self.card_type = ActionCardType.EQUIPMENT_WEAPON

    def effect(self, game: GeniusGame) -> None:
        super().effect(game)