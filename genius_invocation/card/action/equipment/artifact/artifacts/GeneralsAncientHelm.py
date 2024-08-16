from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from .TenacityoftheMillelith import UnmovableMountain
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class GeneralsAncientHelmEntity(Artifact):
    name: str = "General's Ancient Helm"
    name_ch = "将帅兜鍪"
    max_usage = -1
    id = 31200991
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            has_shield = self.from_character.character_zone.has_entity(UnmovableMountain)
            if not has_shield:
                shield = UnmovableMountain(game, from_player=self.from_player, from_character=self.from_character)
                self.from_character.character_zone.add_entity(shield)
            else:
                has_shield.update()

    def update_listener_list(self):
        self.listeners = [
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]

class GeneralsAncientHelm(ArtifactCard):
    id: int = 312009
    name: str = "General's Ancient Helm"
    name_ch = "将帅兜鍪"
    time = 3.5
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = GeneralsAncientHelmEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

