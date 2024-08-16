from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class GladiatorsTriumphusEntity(Artifact):
    id = 31202991
    name: str =  "Gladiator's Triumphus"
    name_ch = "角斗士的凯旋"
    max_usage = 1
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.round_usage = 1

    def on_calculate(self, game: 'GeniusGame'):
        if self.round_usage > 0:
            if game.active_player_index == self.from_player.index:
                if game.current_dice.from_character == self.from_character:
                    if game.current_dice.use_type == SkillType.NORMAL_ATTACK:
                        if game.current_dice.cost[1]['cost_num'] > 0:
                            game.current_dice.cost[1]['cost_num'] -= 1
                            return True
        return False

    def on_skill(self, game: 'GeniusGame'):
        if self.on_calculate(game):
            self.round_usage = 0

    def on_end(self, game: 'GeniusGame'):
        self.round_usage = 1

    def update_listener_list(self):
        self.listeners = [
            (EventType.ON_USE_SKILL, ZoneType.CHARACTER_ZONE, self.on_skill),
            (EventType.CALCULATE_DICE, ZoneType.CHARACTER_ZONE, self.on_calculate),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end)
        ]



class GladiatorsTriumphus(ArtifactCard):
    id: int = 312029
    name: str = "Gladiator's Triumphus"
    name_ch = "角斗士的凯旋"
    time = 4.8
    cost_num: int = 0
    cost_type: CostType = None

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = GladiatorsTriumphusEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

