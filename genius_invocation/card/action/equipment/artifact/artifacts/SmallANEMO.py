from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class SmallANEMO_Entity(SmallElement):
    id = 31250191
    name: str = "Viridescent Venerer's Diadem"
    name_ch = "翠绿的猎人之冠"
    element_type = CostType.ANEMO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)

     

class SmallANEMO(ArtifactCard):
    id: int = 312501
    name: str = "Viridescent Venerer's Diadem"
    name_ch = "翠绿的猎人之冠"
    cost_num: int = 2
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = SmallANEMO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

