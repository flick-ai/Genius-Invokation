from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class InstructorsCapEntity(Artifact):
    name: str = "Instructor's Cap"
    name_ch = "教官的帽子"
    max_usage = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage
        self.round = -1

    def update(self):
        self.usage = self.max_usage

    def on_damage(self, game:'GeniusGame'):
        if self.round != game.round:
            self.round = game.round
            self.usage = self.max_usage
        if self.usage > 0 :
            if game.current_damage.reaction != None:
                if game.current_damage.damage_from == self.from_character:
                    dicetype = ElementToDice(self.from_character.element)
                    self.from_player.dice_zone.add([dicetype.value])
                    self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage)
        ]



class InstructorsCap(ArtifactCard):
    id: int = 312005
    name: str = "Instructor's Cap"
    name_ch = "教官的帽子"
    cost_num: int = 2
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = InstructorsCapEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

