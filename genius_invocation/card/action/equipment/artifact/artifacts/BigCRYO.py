from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement, BigElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class BigCRYO_Entity(BigElement):
    name: str = "Blizzard Strayer"
    name_ch = "冰风迷途的勇士"
    element_type = CostType.CRYO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)


class BigCRYO(ArtifactCard):
    id: int = 312102
    name: str = "Blizzard Strayer"
    name_ch = "冰风迷途的勇士"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = BigCRYO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

