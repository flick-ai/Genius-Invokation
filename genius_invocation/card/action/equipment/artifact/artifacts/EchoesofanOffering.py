from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class EchoesofanOfferingEntity(Artifact):
    name: str =  "Echoes of an Offering"
    name_ch = "来歆余响"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.usage_round = -1
        self.usage_round2 = -1

    def after_skill(self, game:'GeniusGame'):
        if self.usage_round != game.round:
            if game.current_skill.type == SkillType.NORMAL_ATTACK:
                if game.current_skill.from_character == self.from_character:
                    self.from_player.get_card(num=1)
                    self.usage_round = game.round
        if self.usage_round2 != game.round:
             if self.from_player.dice_zone.num() <= self.from_player.hand_zone.num():
                element_dice = ElementToDice[get_my_active_character(game).element]
                self.from_player.dice_zone.add([element_dice.value])
                self.usage_round2 = game.round


    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_USE_SKILL, ZoneType.CHARACTER_ZONE, self.after_skill),
        ]



class EchoesofanOffering(ArtifactCard):
    id: int = 312020
    name: str = "Echoes of an Offering"
    name_ch = "来歆余响"
    cost_num: int = 2
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = EchoesofanOfferingEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

