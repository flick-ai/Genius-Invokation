from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class OceanHuedClamEntity(Artifact):
    name: str = "Ocean-Hued Clam"
    name_ch = "海染砗磲"
    max_usage = 2
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.heal = 0
        self.usage = 0
        self.from_character.heal(heal=3, game=game)

    def update(self):
        pass

    def on_after_heal(self, game:'GeniusGame'):
        if game.current_heal.heal_to_player == self.from_player:
            if self.usage < self.max_usage:
                self.heal += game.current_heal.heal_num
                # self.heal_dict[game.current_heal.heal_to_character]  += 1
                if self.heal >= 3:
                    self.usage += 1
                    self.heal -= 3

    def on_add_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_from == self.from_character:
            game.current_damage.main_damage += self.usage
            self.usage = 0

    def show(self):
        return self.name_ch + ":" + str(self.usage)

    def update_listener_list(self):
        self.listeners = [
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.on_after_heal),
            (EventType.DAMAGE_ADD, ZoneType.CHARACTER_ZONE, self.on_add_damage)
        ]



class OceanHuedClam(ArtifactCard):
    id: int = 312016
    name: str = "Ocean-Hued Clam"
    name_ch = "海染砗磲"
    cost_num: int = 3
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = OceanHuedClamEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

