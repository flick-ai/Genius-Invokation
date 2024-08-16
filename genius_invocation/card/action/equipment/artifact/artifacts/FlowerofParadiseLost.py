from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class FlowerofParadiseLostEntity(Artifact):
    name: str =  "Flower of Paradise Lost"
    name_ch = "乐园遗落之花"
    max_usage = 2
    id = 31202891
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.crowning_crystal = 0
        self.round_usage = 0

    def on_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to.from_player.index == 1- self.from_player.index:
            if game.current_damage.main_damage_element == ElementType.DENDRO or \
                game.current_damage.reaction in [ElementalReactionType.Burning,
                                                ElementalReactionType.Bloom,
                                                ElementalReactionType.Quicken]:
                self.crowning_crystal += 1
                if self.round_usage <= self.max_usage:
                    if self.crowning_crystal >= self.from_player.hand_zone.num():
                        dice = self.from_player.roll_dice(num=1, is_basic=True)
                        self.from_player.dice_zone.add(dice)
                        self.round_usage += 1

    def on_end(self, game: 'GeniusGame'):
        self.round_usage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end)
        ]



class FlowerofParadiseLost(ArtifactCard):
    id: int = 312028
    name: str =  "Flower of Paradise Lost"
    name_ch = "乐园遗落之花"
    time = 4.7
    cost_num: int = 1
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = FlowerofParadiseLostEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

