from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class LuckyDogsSilverCircletEntity(Artifact):
    name: str = "Lucky Dog's Silver Circlet"
    name_ch = "幸运儿银冠"
    max_usage = 1
    id = 31200291
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage
        self.round = -1

    def update(self):
        self.usage = self.max_usage

    def on_after_skill(self, game:'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if self.usage > 0 :
            if game.current_skill.from_character == self.from_character:
                if game.current_skill.type == SkillType.ELEMENTAL_SKILL:
                    self.from_character.heal(heal=2,game=game)
                    self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_after_skill)
        ]



class LuckyDogsSilverCirclet(ArtifactCard):
    id: int = 312002
    name: str = "Lucky Dog's Silver Circlet"
    name_ch = "幸运儿银冠"
    cost_num: int = 2
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = LuckyDogsSilverCircletEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

