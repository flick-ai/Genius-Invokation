from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact, Shield
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer

class Shield_of_Tenacity_of_the_Millelith(Shield):
    name = "Shield_of_Tenacity_of_the_Millelith"
    name_ch = "千岩之盾"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 3

    def update(self):
        self.current_usage = 3


class Tenacity_of_the_Millelith_Entity(Artifact):
    id: int = 312010
    name: str = "Tenacity of the Millelith"
    name_ch = "千岩牢固"
    max_usage = 3
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.round = -1

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            has_shield = self.from_character.character_zone.has_entity(Shield_of_Tenacity_of_the_Millelith)
            if not has_shield:
                shield = Shield_of_Tenacity_of_the_Millelith(game, from_player=self.from_player, from_character=self.from_character)
                self.from_character.character_zone.add_entity(shield)
            else:
                has_shield.update()

    def on_after_damage(self, game:'GeniusGame'):
        if self.round != game.round:
            if self.from_character.is_active and self.from_character.is_alive:
                if game.current_damage.damage_to == self.from_character:
                    element_dice = ElementToDice[self.from_character.element]
                    self.from_player.dice_zone.add([element_dice.value])
                    self.round = game.round

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_TAKES_DMG, ZoneType.CHARACTER_ZONE, self.on_after_damage),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]


class Tenacity_of_the_Millelith(ArtifactCard):
    id: int = 312010
    name: str = "Tenacity of the Millelith"
    name_ch = "千岩牢固"
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = Tenacity_of_the_Millelith_Entity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

        # self.usages = defaultdict(int)

