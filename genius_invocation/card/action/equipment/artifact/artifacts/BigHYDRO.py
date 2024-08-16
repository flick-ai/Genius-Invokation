from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement, BigElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class BigHYDRO_Entity(BigElement):
    name: str = "Heart of Depth"
    name_ch = "沉沦之心"
    id = 31220291
    element_type = CostType.HYDRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)


class BigHYDRO(ArtifactCard):
    id: int = 312202
    name: str = "Heart of Depth"
    name_ch = "沉沦之心"
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = BigHYDRO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

