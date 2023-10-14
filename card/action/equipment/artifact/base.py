from utils import *
from ..base import EquipmentCard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game import GeniusGame


class ArtifactCard(EquipmentCard):
    # 圣遗物牌

    def __init__(self) -> None:
        super().__init__()

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)
        self.character.artifact_card = self