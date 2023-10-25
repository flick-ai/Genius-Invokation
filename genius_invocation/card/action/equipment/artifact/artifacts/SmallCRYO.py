from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard, SmallElement
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class SmallCRYO_Entity(SmallElement):
    name: str = "Broken Rime's Echo"
    name_ch = "破冰踏雪的回音"
    element_type = CostType.CRYO
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)

     

class SmallCRYO(ArtifactCard):
    id: int = 312101
    name: str = "Broken Rime's Echo"
    name_ch = "破冰踏雪的回音"
    cost_num: int = 2
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = SmallCRYO_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

