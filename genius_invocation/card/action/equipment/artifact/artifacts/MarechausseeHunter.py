from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class MarechausseeHunterEntity(Artifact):
    name: str =  "Marechaussee Hunter"
    name_ch = "逐影猎人"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.round_usage = 0

    def excute(self, game):
        if self.round_usage == 0 or self.round_usage == 3:
            self.round_usage += 1
            element_dice = ElementToDice[get_my_active_character(game).element]
            self.from_player.dice_zone.add([element_dice.value])
            return
        if self.round_usage == 1:
            self.round_usage += 1
            self.from_player.get_card(num=1)
            return


    def after_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            self.excute(game)

    def after_heal(self, game:'GeniusGame'):
        if game.current_heal.heal_to_character == self.from_character:
            self.excute(game)

    def on_end(self, game: 'GeniusGame'):
        self.round_usage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.after_heal),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end)
        ]



class MarechausseeHunter(ArtifactCard):
    id: int = 312024
    name: str = "Marechaussee Hunter"
    name_ch = "逐影猎人"
    cost_num: int = 3
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = MarechausseeHunterEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

