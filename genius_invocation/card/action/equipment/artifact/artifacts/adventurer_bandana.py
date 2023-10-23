from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class AdventurerBandana_Entity(Artifact):
    id: int = 0
    name: str = "Adventurer's Bandana"
    name_ch = "冒险家头巾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)


class AdventurerBandana(ArtifactCard):
    '''冒险家头巾'''
    id: int = 0
    name: str = "Adventurer's Bandana"
    name_ch = "冒险家头巾"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = AdventurerBandana_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

        # self.usages = defaultdict(int)

