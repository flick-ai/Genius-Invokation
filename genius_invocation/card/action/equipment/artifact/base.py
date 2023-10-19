from genius_invocation.utils import *
from genius_invocation.card.action.equipment.base import EquipmentCard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame


class ArtifactCard(EquipmentCard):
    # 圣遗物牌

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        pass
