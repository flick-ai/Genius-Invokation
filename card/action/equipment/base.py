from ..base import ActionCard
from typing import TYPE_CHECKING
from entity.entity import Entity
from utils import *

if TYPE_CHECKING:
    from game.game import GeniusGame
    from game.zone import CharacterZone
    from game.player import GeniusPlayer
    from entity.status import Status, Equipment
class EquipmentCard(ActionCard):
    # 装备牌基本类
    equipment_entity: Equipment
    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        pass