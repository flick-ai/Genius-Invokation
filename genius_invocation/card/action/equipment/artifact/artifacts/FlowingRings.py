from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class FlowingRingsEntity(Artifact):
    name: str = "Flowing Rings"
    name_ch = "浮溯之珏"
    id = 31201991
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage_round = -1

    def after_skill(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                if game.current_skill.from_character == self.from_character:
                    self.from_player.get_card(num=1)
                    self.usage_round = game.round

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
        ]



class FlowingRings(ArtifactCard):
    id: int = 312019
    name: str = "Flowing Rings"
    name_ch = "浮溯之珏"
    time = 4.3
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = FlowingRingsEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

