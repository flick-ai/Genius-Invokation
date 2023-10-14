from utils import *
from typing import TYPE_CHECKING
from ..base import EquipmentCard

if TYPE_CHECKING:
    from game.game import GeniusGame


class WeaponCard(EquipmentCard):
    # 武器牌
    weapon_type: WeaponType
    def __init__(self) -> None:
        super().__init__()
        self.card_type = ActionCardType.EQUIPMENT_WEAPON

    def effect(self, game: 'GeniusGame') -> None:
        super().effect(game)