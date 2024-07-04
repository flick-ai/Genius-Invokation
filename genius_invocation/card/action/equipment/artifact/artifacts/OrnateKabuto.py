from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class OrnateKabutoEntity(Artifact):
    name: str = "Ornate Kabuto"
    name_ch = "华饰之兜"
    max_usage = -1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)

    def update(self):
        pass

    def on_after_skill(self, game:'GeniusGame'):
        if game.current_skill.from_character.from_player == self.from_player:
            if game.current_skill.from_character != self.from_character:
                if game.current_skill.type == SkillType.ELEMENTAL_BURST:
                    self.from_character.get_power(power=1)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill)
        ]



class OrnateKabuto(ArtifactCard):
    id: int = 312007
    name: str = "Ornate Kabuto"
    name_ch = "华饰之兜"
    time = 3.5
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = OrnateKabutoEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

