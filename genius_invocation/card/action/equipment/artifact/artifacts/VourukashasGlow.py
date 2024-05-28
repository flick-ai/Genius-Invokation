from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class VourukashasGlowEntity(Artifact):
    name: str =  "Vourukasha's Glow"
    name_ch = "花海甘露之光"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage_round = -1

    def after_damage(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_damage.damage_to == self.from_character:
                if self.from_character.is_active:
                    self.from_player.get_card(num=1)
                    self.usage_round = game.round

    def on_end(self, game: 'GeniusGame'):
        if game.active_player_index == self.from_player.index:
            if self.usage_round == game.round:
                self.from_character.heal(1, game)

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.END_PHASE, ZoneType.CHARACTER_ZONE, self.on_end)
        ]



class VourukashasGlow(ArtifactCard):
    id: int = 312022
    name: str = "Vourukasha's Glow"
    name_ch = "花海甘露之光"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = VourukashasGlowEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

