from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class ShadowoftheSandKingEntity(Artifact):
    name: str = "Shadow of the Sand King"
    name_ch = "沙王的投影"
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.from_player.get_card(num=1)
        self.usage_round = -1

    def on_damage(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_damage.damage_to.from_player != self.from_player:
                if game.current_damage.reaction != None:
                    self.from_player.get_card(num=1)
                    self.usage_round = game.round

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage),
        ]



class ShadowoftheSandKing(ArtifactCard):
    id: int = 312017
    name: str = "Shadow of the Sand King"
    name_ch = "沙王的投影"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = ShadowoftheSandKingEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

