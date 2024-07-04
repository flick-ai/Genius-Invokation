from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class HeartofKhvarenasBrillianceEntity(Artifact):
    name: str =  "Heart of Khvarena's Brilliance"
    name_ch = "灵光明烁之心"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage_round = -1
        self.is_excute = False

    def after_damage(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_damage.damage_to == self.from_character:
                self.is_excute = True
    
    def on_excute(self, game: 'GeniusGame'):
        if self.is_excute:
            if self.from_character.is_active and self.from_character.is_alive:
                self.from_player.get_card(num=1)
                self.is_excute = False

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_excute)
        ]



class HeartofKhvarenasBrilliance(ArtifactCard):
    id: int = 312021
    name: str = "Heart of Khvarena's Brilliance"
    name_ch = "灵光明烁之心"
    time = 4.3
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = HeartofKhvarenasBrillianceEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

