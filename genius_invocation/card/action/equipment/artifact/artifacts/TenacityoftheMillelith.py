from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact, Shield
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class UnmovableMountain(Shield):
    name = "Unmovable Mountain"
    name_ch = "重嶂不移"
    id = 31201041
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character=None):
        super().__init__(game, from_player, from_character)
        self.current_usage = 2

    def update(self):
        self.current_usage = 2

class TenacityoftheMillelithEntity(Artifact):
    name: str = "Tenacity of the Millelith"
    name_ch = "千岩牢固"
    max_usage = 1
    id = 31201091
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.round = -1
        self.return_dice = False

    def on_begin(self, game: 'GeniusGame'):
        if game.active_player == self.from_player:
            has_shield = self.from_character.character_zone.has_entity(UnmovableMountain)
            if not has_shield:
                shield = UnmovableMountain(game, from_player=self.from_player, from_character=self.from_character)
                self.from_character.character_zone.add_entity(shield)
            else:
                has_shield.update()

    def on_after_damage(self, game:'GeniusGame'):
        if self.round != game.round:
            if game.current_damage.damage_to == self.from_character:
                self.return_dice = True
                self.round = game.round

    def on_final_excute(self, game:'GeniusGame'):
        if self.return_dice:
            if self.from_character.is_active and self.from_character.is_alive:
                element_dice = ElementToDice[self.from_character.element]
                self.from_player.dice_zone.add([element_dice.value])
                self.return_dice = False


    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.on_after_damage),
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_final_excute),
            (EventType.BEGIN_ACTION_PHASE, ZoneType.CHARACTER_ZONE, self.on_begin)
        ]




class TenacityoftheMillelith(ArtifactCard):
    id: int = 312010
    name: str = "Tenacity of the Millelith"
    name_ch = "千岩牢固"
    time = 3.7
    cost_num: int = 3
    cost_type: CostType = CostType.WHITE

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = TenacityoftheMillelithEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

