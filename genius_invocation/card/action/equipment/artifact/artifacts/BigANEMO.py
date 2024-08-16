from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement, BigElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class BigANEMO_Entity(BigElement):
    name: str = "Viridescent Venerer"
    name_ch = "翠绿之影"
    element_type = CostType.ANEMO
    id = 31250291
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)


class BigANEMO(ArtifactCard):
    id: int = 312502
    name: str = "Viridescent Venerer"
    name_ch = "翠绿之影"
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = BigANEMO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

