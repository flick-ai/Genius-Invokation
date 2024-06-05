from genius_invocation.utils import *
from genius_invocation.card.action.equipment.artifact.base import ArtifactCard
from genius_invocation.entity.status import Artifact
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from genius_invocation.game.game import GeniusGame
    from genius_invocation.game.player import GeniusPlayer


class VeteransVisageEntity(Artifact):
    name: str =  "Veteran's Visage"
    name_ch = "老兵的容颜"
    def __init__(self, game: 'GeniusGame', from_player: 'GeniusPlayer', from_character = None, artifact_card = None):
        super().__init__(game, from_player, from_character, artifact_card)
        self.round_usage = 0
        self.is_excute = False

    def excute(self, game):
        if self.round_usage == 0:
            self.round_usage += 1
            element_dice = ElementToDice[get_my_active_character(game).element]
            self.from_player.dice_zone.add([element_dice.value])
            return
        if self.round_usage == 1:
            self.round_usage += 1
            self.from_player.get_card(num=1)
            return
        
    def on_excute(self, game):
        if self.is_excute:
            if self.from_character.is_alive:
                self.is_excute = False
                self.excute(game)

    def after_damage(self, game:'GeniusGame'):
        if game.current_damage.damage_to == self.from_character:
            self.is_excute = True

    def after_heal(self, game:'GeniusGame'):
        if game.current_heal.heal_to_character == self.from_character:
            self.excute(game)

    def on_end(self, game: 'GeniusGame'):
        self.round_usage = 0

    def update_listener_list(self):
        self.listeners = [
            (EventType.EXECUTE_DAMAGE, ZoneType.CHARACTER_ZONE, self.after_damage),
            (EventType.AFTER_HEAL, ZoneType.CHARACTER_ZONE, self.after_heal),
            (EventType.FINAL_END, ZoneType.CHARACTER_ZONE, self.on_end),
            (EventType.FINAL_EXECUTE, ZoneType.CHARACTER_ZONE, self.on_excute),
        ]



class VeteransVisage(ArtifactCard):
    id: int = 312023
    name: str = "Veteran's Visage"
    name_ch = "老兵的容颜"
    cost_num: int = 2
    cost_type: CostType = CostType.BLACK

    def __init__(self) -> None:
        super().__init__()
        self.artifact_entity = VeteransVisageEntity

    def on_played(self, game: 'GeniusGame') -> None:
        super().on_played(game)

