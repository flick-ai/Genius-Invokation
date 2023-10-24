from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement, BigElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class BigDENDRO_Entity(BigElement):
    name: str = "Deepwood Memories"
    name_ch = "深林的记忆"
    element_type = CostType.DENDRO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)


class BigDENDRO(ArtifactCard):
    id: int = 312702
    name: str = "Deepwood Memories"
    name_ch = "深林的记忆"
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = BigDENDRO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

