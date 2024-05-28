from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class GildedDreamsEntity(Artifact):
    name: str = "Gilded Dreams"
    name_ch = "饰金之梦"
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        num = 1
        if len(self.from_player.element_set) == 3:
            num = 2
        element_dice = ElementToDice[get_my_active_character(game).element]
        self.from_player.dice_zone.add([element_dice.value for _ in range(num)])
        self.usage = self.max_usage

    def on_damage(self, game:'GeniusGame'):
        if self.usage > 0:
            if game.current_damage.damage_to.from_player != self.from_player:
                if game.current_damage.reaction != None:
                    self.from_player.get_card(num=1)
                    self.usage -= 1

    def on_end(self, game: 'GeniusGame'):
        self.usage = self.max_usage

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_damage),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
        ]



class GildedDreams(ArtifactCard):
    id: int = 312018
    name: str = "Gilded Dreams"
    name_ch = "饰金之梦"
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = GildedDreamsEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

