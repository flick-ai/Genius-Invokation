from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class GamblersEarringsEntity(Artifact):
    name: str = "Gambler's Earrings"
    name_ch = "赌徒的耳环"
    max_usage = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage = self.max_usage

    def on_die(self, game:'GeniusGame'):
        if self.usage > 0 :
            if game.current_die.from_player != self.from_player:
                if self.from_character.is_active:
                    self.from_player.dice_zone.add([DiceType.OMNI.value, DiceType.OMNI.value])
                    self.usage -= 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.CHARACTER_DIE, ZoneType.CHARACTER_ZONE, self.on_die)
        ]



class GamblersEarrings(ArtifactCard):
    id: int = 312004
    name: str = "Gambler's Earrings"
    name_ch = "赌徒的耳环"
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = GamblersEarringsEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

    @staticmethod
    def balance_adjustment():
        log = {}
        log[3.8] = "调整了「七圣召唤」中，装备牌「赌徒的耳环」效果：现在该装备牌的效果整场牌局限制3次"
        return log

